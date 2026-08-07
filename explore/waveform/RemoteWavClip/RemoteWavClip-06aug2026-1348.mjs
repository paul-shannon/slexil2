/**
 * RemoteWavClip — pulls a [startMs, endMs] slice out of a remote WAV file
 * and reconstructs it as a standalone, valid WAV Blob.
 *
 * Node vs browser: this file is meant to run unchanged in both. The only
 * browser-only call (URL.createObjectURL) is isolated behind a small
 * seam so it can be swapped for a Node equivalent (e.g. fs.writeFileSync)
 * during testing.
 */

class RemoteWavClip {

  #url;
  #startMs;
  #endMs;
  #header;
  #httpStatus;
  #clipSpecs;

  //--------------------------------------------------------------------------------
  constructor(url, startMs, endMs) {
    this.#url = url;
    this.#startMs = startMs;
    this.#endMs = endMs;
    this.#header = null;
    this.#httpStatus = null;
    this.#clipSpecs = null;
    }

  //--------------------------------------------------------------------------------
  getUrl()     {return this.#url;}
  getStartMs() {return this.#startMs;}
  getEndMs()   {return this.#endMs;}
  getHttpStatus() {return this.#httpStatus;}

  //--------------------------------------------------------------------------------
  async urlExists() {
    try {
       //console.log("---- RemoteWavClip.mjs, urlExists? " + this.#url)
       const result = await fetch(this.#url, { method: 'HEAD' });
       console.log(" --- urlExists status: " + result.status);
       this.#httpStatus = result.status;
       return ![404, 500].includes(result.status)
       } catch (err) {
            // network failure, DNS failure, CORS block, offline, etc. —
            // fetch() rejects rather than resolving with a status in these cases
         return false;
        }
    } // urlExists

  //--------------------------------------------------------------------------------
  async getHeader(){
    const SCAN_WINDOW = 65536;
    console.log("RWC.probe, about to fetch " + this.#url)
    const header = await fetch(
          this.#url, {headers: {Range: `bytes=0-${SCAN_WINDOW - 1}`}});
    console.log("header fetch status: " + header.status)
    this.#httpStatus = header.status

    const buf = await header.arrayBuffer();
    const view = new DataView(buf);
       // 1 = PCM, 3 = IEEE float, 0xFFFE = extensible
    
    const audioFormat = view.getUint16(20, true); 
    const numChannels = view.getUint16(22, true);
    const sampleRate = view.getUint32(24, true);
    const bitDepth = view.getUint16(34, true);
    // const dataSize = view.getUint32(40, true);
    console.log("dataSize: " + dataSize)

    const map = new Map();
    map.set("audioFormat", audioFormat);
    map.set("numberOfChannels", numChannels);
    map.set("sampleRate", sampleRate);
    map.set("bitDepth", bitDepth);
    map.set("fileSize", dataSize);
    this.#clipSpecs = map;
    return(map)
    }

  //--------------------------------------------------------------------------------
  async probe(){
    const SCAN_WINDOW = 65536;
    console.log("RWC.probe, about to fetch " + this.#url)
    const result = await fetch(
          this.#url, {headers: {Range: `bytes=0-${SCAN_WINDOW - 1}`}});
    this.#httpStatus = result.status;
    console.log("RWC.probe, httpStatus: " + this.#httpStatus);
    if(!result.ok && result.status !== 206) {
      throw new Error(`Header range fetch failed: ${result.status} (server may not support byte ranges)`);
      }
    if (result.status !== 206) {
      console.warn('RemoteWavClip: server returned the full file instead of a partial range for the header fetch. Byte-range support may be misconfigured.');
      }

    console.log("--- numChannels: " + numChannels);
    console.log("--- sampleRate:  " + sampleRate);
    console.log("--- bitDepth:    " + bitDepth);
    return(map);
    }
  //--------------------------------------------------------------------------------

} // class RemoteWavClip

export default RemoteWavClip;
