import test from 'node:test';
import assert from 'node:assert';
import {state} from '../appState.mjs'; 

//--------------------------------------------------------------------------------
test('constructor simply creates the internal data structure, currently a Map', () => {

  console.log("--- testing appState constructor");
  assert.equal(state.size(), 0)
  });

//--------------------------------------------------------------------------------
test('setters and getters', () => {

  console.log("--- testing appState setters and getters");

  state.clear()
  assert.equal(state.size(), 0)
  state.set("x", 1)
  state.set("y", "2")
  state.set("z", [1,2,3])
  assert.equal(state.size(),3)

  const x = state.get("x")
  assert.equal(x, 1)

  const y = state.get("y")
  assert.equal(y, "2")

  const z = state.get("z")
  assert.deepEqual(z, [1,2,3])

  });

//--------------------------------------------------------------------------------
test('keys', () => {

  console.log("--- testing appState keys");
  
  state.clear()
  assert.equal(state.size(), 0)
  state.set("x", 1)
  state.set("z", [1,2,3])
  state.set("y", "2")

  assert.deepEqual(state.keys(), ["x", "z", "y"])
  assert.equal(state.hasKey("x"), true)
  assert.equal(state.hasKey("xyz"), false)

});
//--------------------------------------------------------------------------------
