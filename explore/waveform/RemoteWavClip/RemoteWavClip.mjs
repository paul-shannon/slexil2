/**
 * RemoteWavClip — pulls a [startMs, endMs] slice out of a remote WAV file
 * and reconstructs it as a standalone, valid WAV Blob.
 *
 * Node vs browser: this file is meant to run unchanged in both. Just one
 * browser-only call (URL.createObjectURL) is isolated behind a small
 * seam (see retrieve()) so it degrades gracefully in Node instead of throwing.
 */

import {state} from './appState.mjs'

class RemoteWavClip {
  #url;
  #startMs;
  #endMs;
  #httpStatus;
  #blob;        // reconstructed WAV Blob, set by probe()
  #objectUrl;   // browser-only Object URL for #blob, set by probe()
  //--------------------------------------------------------------------------------
  constructor(url, startMs, endMs) {
    console.log(" --- RWC ctor");
    console.log("url: " + url)
    console.log("startMs: " + startMs);
    console.log("endMs: " + endMs);
    this.#url = url;
    this.#startMs = startMs;
    this.#endMs = endMs;
    this.#httpStatus = null;
    this.#blob = null;
    this.#objectUrl = null;
    }

  //--------------------------------------------------------------------------------
  getUrl()        { return this.#url; }
  getStartMs()    { return this.#startMs; }
  getEndMs()      { return this.#endMs; }
  getHttpStatus() { return this.#httpStatus; }
  getBlob()       { return this.#blob; }
  getObjectUrl()  { return this.#objectUrl; }
  //--------------------------------------------------------------------------------
  async urlExists() {
    try {
      console.log("--- RWC.urlExists, fetching only HEAD")
      this.#httpStatus = 404;  // pessimistically
      const result = await fetch(this.#url, { method: 'HEAD' });
      this.#httpStatus = result.status;
      console.log("  urlExists, httpStatus: ")
      console.log(this.#httpStatus)
      return ![404, 500].includes(result.status);
    } catch (err) {
      // network failure, DNS failure, CORS block, offline, etc. —
      // fetch() rejects rather than resolving with a status in these cases
      return false;
    }
  } // urlExists
  //--------------------------------------------------------------------------------
  /** Fetches and parses format info: codec, sample rate, bit depth, channel
   *  count, plus the byte offset/size of the 'data' chunk (needed to compute
   *  byte ranges for probe()) and derived fileSize/durationMs. */
  async getMetadata() {
    console.log("--- RWC.getMetadata");
    console.log("     url: " + this.#url);
    const SCAN_WINDOW = 65536;
    const res = await fetch(
      this.#url, { headers: { Range: `bytes=0-${SCAN_WINDOW - 1}` } });
    console.log("     result status: " + res.status)
    this.#httpStatus = res.status;

    if (!res.ok && res.status !== 206) {
      throw new Error(`Header range fetch failed: ${res.status} (server may not support byte ranges)`);
      }
    if (res.status == 206){
      console.log("  result status: 206 partial content ")
      }
    else{
      console.warn('RemoteWavClip: server returned the full file instead of a partial range for the header fetch. Byte-range support may be misconfigured.');
      }

    const buf = await res.arrayBuffer();
    const view = new DataView(buf);

    const audioFormat = view.getUint16(20, true); // 1=PCM, 3=float, 0xFFFE=extensible
    const numChannels = view.getUint16(22, true);
    const sampleRate  = view.getUint32(24, true);
    const bitDepth    = view.getUint16(34, true);

      // Metadata chunks (LIST/INFO, bext, iXML, etc.) can push 'data' out well
      // past byte 44, so scan for it rather than assuming a fixed offset.
    let offset = 12;
    let dataOffset = null;
    let dataSize = null;
    while (offset < buf.byteLength - 8) {
      const id = String.fromCharCode(
        view.getUint8(offset), view.getUint8(offset + 1),
        view.getUint8(offset + 2), view.getUint8(offset + 3));
      const size = view.getUint32(offset + 4, true);
      if (id === 'data') {
        dataOffset = offset + 8;
        dataSize = size;
        break;
        }
      offset += 8 + size + (size % 2); // chunks are word-aligned
      } // while

    if (dataOffset === null) {
      throw new Error(`RemoteWavClip: could not locate 'data' chunk within the first ${SCAN_WINDOW} bytes.`);
      }

    const byteRate = sampleRate * numChannels * (bitDepth / 8);
    const durationMs = (dataSize / byteRate) * 1000;
    const msecs =  Number(durationMs.toFixed(0));
    const durationMinutes = durationMs/(1000 * 60)
    const minutes = Number(durationMinutes.toFixed(2))

    const map = new Map();

    map.set("audioFormat", audioFormat);
    map.set("numberOfChannels", numChannels);
    map.set("sampleRate", sampleRate);
    map.set("bitDepth", bitDepth);
    map.set("dataOffset", dataOffset);
    map.set("dataSize", dataSize);
    map.set("durationMs", msecs);
    map.set("durationMinutes", minutes);
    state.set("wavMetaData", map)
    return map;

  } // getMetadata
  //--------------------------------------------------------------------------------
  /** Fetches the [startMs, endMs] audio byte range and rebuilds it as a
   *  standalone, valid WAV Blob. 
   *  yet. In a browser, also creates an Object URL for the blob
   *  (see getObjectUrl()); in Node, that step is skipped rather than
   *  thrown, since URL.createObjectURL doesn't exist there. 
   */

  async retrieve() {
    console.log("--- entering RWC.retrieve")
    if (!state.hasKey("wavMetaData")){
      throw new Error("RemoteWavClip.retrieve: metadata must exist before clip retrieval")
      }
    const metadata = state.get("wavMetaData")
    const dataOffset = metadata.get("dataOffset");
    const sampleRate = metadata.get("sampleRate");
    const bitDepth = metadata.get("bitDepth");
    const numChannels = metadata.get("numberOfChannels");
    const blockAlign = (bitDepth / 8) * numChannels;

    const startByte = dataOffset + Math.floor((this.#startMs / 1000) * sampleRate) * blockAlign;
    const endByte = dataOffset + Math.floor((this.#endMs / 1000) * sampleRate) * blockAlign - 1;

    const res = await fetch(this.#url, { headers: { Range: `bytes=${startByte}-${endByte}` } });
    this.#httpStatus = res.status;
    if (!res.ok && res.status !== 206) {
      throw new Error(`Clip range fetch failed: ${res.status}`);
    }
    const raw = await res.arrayBuffer();

    this.#blob = RemoteWavClip.#buildWavBlob(raw, { sampleRate, numChannels, bitDepth });

      // Browser-only seam: skip gracefully in Node rather than throwing.
    this.#objectUrl = (typeof URL !== 'undefined' && typeof URL.createObjectURL === 'function')
      ? URL.createObjectURL(this.#blob)
      : null;

    return this.#blob;

  } // retrieve
  //--------------------------------------------------------------------------------
  /* Call when this clip's Blob/Object URL is no longer needed. 
   */
  revoke() {
    if (this.#objectUrl) URL.revokeObjectURL(this.#objectUrl);
  }
  //--------------------------------------------------------------------------------
  static #buildWavBlob(pcmBuffer, {sampleRate, numChannels, bitDepth}) {

    const blockAlign = numChannels * (bitDepth / 8);
    const byteRate = sampleRate * blockAlign;
    const dataSize = pcmBuffer.byteLength;

    const header = new ArrayBuffer(44);
    const view = new DataView(header);
    const writeStr = (offset, str) => {
      for (let i = 0; i < str.length; i++) view.setUint8(offset + i, str.charCodeAt(i));
    };

    writeStr(0, 'RIFF');
    view.setUint32(4, 36 + dataSize, true);
    writeStr(8, 'WAVE');
    writeStr(12, 'fmt ');
    view.setUint32(16, 16, true);
    view.setUint16(20, 1, true); // PCM
    view.setUint16(22, numChannels, true);
    view.setUint32(24, sampleRate, true);
    view.setUint32(28, byteRate, true);
    view.setUint16(32, blockAlign, true);
    view.setUint16(34, bitDepth, true);
    writeStr(36, 'data');
    view.setUint32(40, dataSize, true);

    return new Blob([header, pcmBuffer], { type: 'audio/wav' });

    } // #buildWavBlog

} // class RemoteWavClip

export default RemoteWavClip;
