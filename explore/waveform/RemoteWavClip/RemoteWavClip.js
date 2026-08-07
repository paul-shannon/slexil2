class RemoteWavClip {
  #url;
  #startMs;
  #endMs;

  constructor(url, startMs, endMs) {
    this.#url = url;
    this.#startMs = startMs;
    this.#endMs = endMs;
  }

  get url() { return this.#url; }
  get startMs() { return this.#startMs; }
  get endMs() { return this.#endMs; }
}

module.exports = RemoteWavClip; // or `export default` if you're using ESM in Node
