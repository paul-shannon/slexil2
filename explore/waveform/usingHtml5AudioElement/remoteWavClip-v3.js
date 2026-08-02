/**
 * RemoteWavClip — pulls a [startMs, endMs] slice out of a remote WAV file
 * (byte-range + CORS enabled server) and reconstructs it as a standalone,
 * valid WAV Blob with its own Object URL. Hand that URL to a real <audio>
 * element, then point WaveSurfer at that element (its "media" option) so
 * WaveSurfer renders the waveform while the native element does playback.
 *
 * Usage:
 *   const clip = await RemoteWavClip.create(url, 12000, 17000);
 *   audioEl.src = clip.url;
 *   const ws = WaveSurfer.create({ container: '#waveform', media: audioEl });
 *   // ...when moving to the next line:
 *   clip.revoke();
 */
class RemoteWavClip {
  static _headerCache = new Map(); // url -> {numChannels, sampleRate, bitDepth, dataOffset}

  static async create(url, startMs, endMs) {
    console.log("remoteWavClip-v3, create: " + url + " from " + startMs + " to " + endMs);
    const header = await this._getHeader(url);
    const {numChannels, sampleRate, bitDepth, dataOffset, audioFormat} = header;
    const blockAlign = (bitDepth / 8) * numChannels;

    const startByte = dataOffset + Math.floor((startMs / 1000) * sampleRate) * blockAlign;
    const endByte = dataOffset + Math.floor((endMs / 1000) * sampleRate) * blockAlign - 1;

    const res = await fetch(url, { headers: { Range: `bytes=${startByte}-${endByte}` } });
    if (!res.ok && res.status !== 206) throw new Error(`Range fetch failed: ${res.status}`);
    const raw = await res.arrayBuffer();

    let pcm = raw;
    let outputBitDepth = bitDepth;

    console.log("remoteWavClip-v3.js, audioFormat: " + audioFormat)
    const blob = this._buildWavBlob(pcm, {sampleRate, numChannels, bitDepth: outputBitDepth});
    return new RemoteWavClip(blob);
    }

  constructor(blob) {
    this.blob = blob;
    this.url = URL.createObjectURL(blob);
    console.log("RemoteWavClip ctor, new url: " + this.url)
    }

  revoke() {
    URL.revokeObjectURL(this.url);
    }

  static _buildWavBlob(pcmBuffer, { sampleRate, numChannels, bitDepth }) {
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
    const result = new Blob([header, pcmBuffer], { type: 'audio/wav' });
    console.log("built, new blob: ")
    console.log(result)
    return(result)
  }

  /** Fetch + cache format info (sample rate, channels, bit depth, data chunk offset). */
  static async _getHeader(url) {
    if (this._headerCache.has(url)) return this._headerCache.get(url);

    // Metadata chunks (LIST/INFO, bext, iXML, etc.) can push 'data' out
    // much further than a minimal 44-byte header, so scan a generous
    // window (64KB) rather than assuming it's always near the front.
    const SCAN_WINDOW = 65536;
    const res = await fetch(url, { headers: { Range: `bytes=0-${SCAN_WINDOW - 1}` } });
    if (!res.ok && res.status !== 206) {
      throw new Error(`Header range fetch failed: ${res.status} (server may not support byte ranges)`);
    }
    if (res.status !== 206) {
      console.warn('RemoteWavClip: server returned the full file instead of a partial range for the header fetch. Byte-range support may be misconfigured.');
    }
    const buf = await res.arrayBuffer();
    const view = new DataView(buf);

    const audioFormat = view.getUint16(20, true); // 1 = PCM, 3 = IEEE float, 0xFFFE = extensible
    const numChannels = view.getUint16(22, true);
    const sampleRate = view.getUint32(24, true);
    const bitDepth = view.getUint16(34, true);
    console.log("--- audioFormat: " + audioFormat)
    console.log("--- numChannels: " + numChannels)
    console.log("--- sampleRate:  " + sampleRate);
    console.log("--- bitDepth:    " + bitDepth)

    if (audioFormat === 6 || audioFormat === 7) {
      console.info(`RemoteWavClip: source is G.711 ${audioFormat === 6 ? 'A-law' : 'mu-law'} (format ${audioFormat}); decoding to linear PCM.`);
    } else if (audioFormat !== 1 && audioFormat !== 0xFFFE) {
      console.warn(`RemoteWavClip: source audioFormat code is ${audioFormat} (not standard PCM, and not a handled companded format). Playback may not sound correct since the rebuilt header always declares linear PCM.`);
    }

    // Scan chunks after the 12-byte RIFF/WAVE header to find 'data'.
    let offset = 12;
    let dataOffset = null;
    while (offset < buf.byteLength - 8) {
      const id = String.fromCharCode(
        view.getUint8(offset), view.getUint8(offset + 1),
        view.getUint8(offset + 2), view.getUint8(offset + 3)
        );
      const size = view.getUint32(offset + 4, true);
      if (id === 'data') { dataOffset = offset + 8; break; }
      offset += 8 + size + (size % 2);
      } // while

    if (dataOffset === null)
      throw new Error(`RemoteWavClip: could not locate 'data' chunk within the first ${SCAN_WINDOW} bytes. Increase SCAN_WINDOW.`);

    const info = { numChannels, sampleRate, bitDepth, dataOffset, audioFormat };
    this._headerCache.set(url, info);
    return info;
    } // _getHeader

} // class RemoteWavClip
