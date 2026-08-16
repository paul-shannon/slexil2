class State{
  #map;
  constructor(){
    this.#map = new Map();
    }
   size() {
    return this.#map.size;
    }
  set(key, value) {
    this.#map.set(key, value);
    }
  get(key) {
    return this.#map.get(key);
    }
  keys() {
     return Array.from(this.#map.keys())
     }
  hasKey(key) {
     return this.#map.has(key)
     }
  clear() {
     this.#map = new Map();
     }
} // class State

const state = new State();
export {state};
