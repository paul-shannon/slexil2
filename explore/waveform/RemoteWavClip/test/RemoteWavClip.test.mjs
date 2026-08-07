import test from 'node:test';
import assert from 'node:assert/strict';
import RemoteWavClip from '../RemoteWavClip.mjs';

//--------------------------------------------------------------------------------
test('constructor stores url, startMs, endMs and exposes them via getters', () => {

  console.log("--- testing constructor");

  const clip = new RemoteWavClip('https://example.com/file.wav', 2000, 4000);

  assert.equal(clip.getUrl(), 'https://example.com/file.wav');
  assert.equal(clip.getStartMs(), 2000);
  assert.equal(clip.getEndMs(), 4000);
  });

//--------------------------------------------------------------------------------
test('private fields are not accessible from outside the class', () => {

  console.log("--- testing for private fields");

  const clip = new RemoteWavClip('https://example.com/file.wav', 0, 1000);

  // #url is a true private field: it doesn't show up as an own property
  assert.equal(Object.keys(clip).length, 0);
  assert.equal(clip['#url'], undefined);

});
//--------------------------------------------------------------------------------
//test('probe discovers and stores codec, sampling rate & depth, numberOfChannels',
//    async () => {
//
//  console.log("--- testing probe for wav attributes");
//
//  const clip = new RemoteWavClip("https://pshannon.net/tmp/new.wav", 0, 1000);
//  const x = await clip.probe()
//  // assert.equal(x, "fubar")
//  })
//--------------------------------------------------------------------------------
test('urlExists', async () => {

  var url = "https://pshannon.net/bogus.wav"
  console.log("--- testing urlExists: " + url);

  var clip = new RemoteWavClip(url, 0, 1000);
  var exists = await clip.urlExists();
  assert.equal(clip.getHttpStatus(), 404)
  console.log(" urlExists? " + exists)
  assert.equal(exists, false)

  url = "https://pshannon.net/tmp/new.wav"
  console.log("--- testing urlExists: " + url);
  clip = new RemoteWavClip(url, 0, 1000);
  exists = await clip.urlExists();
  assert.equal(exists, true)

  url = "https://pshannon-bogus.net/tmp/new.wav"
  console.log("--- testing urlExists: " + url);
  clip = new RemoteWavClip(url, 0, 1000);
  exists = await clip.urlExists();
  assert.equal(exists, false)

})
//--------------------------------------------------------------------------------
test('getHeader.daylight', async () => {

  console.log("--- testing getHeader.daylight");

  const url = "https://pshannon.net/tmp/new.wav"
  const clip = new RemoteWavClip(url, 0, 1000);
  const header = await clip.getHeader()
  console.log("--- status: " + clip.getHttpStatus())

  assert.ok(header instanceof Map);
  const keys = Array.from(header.keys()).sort()


  console.log(keys);
  assert.deepStrictEqual(keys, ['audioFormat', 'bitDepth',
                                'dataOffset', 'dataSize',
                                'durationMinutes', 'durationMs',
                                'fileSize',
                                'numberOfChannels', 'sampleRate'])
  console.log("------ daylight header");
  for(const key of keys){
    console.log(key + ": " + header.get(key))
    }

  assert.ok(header.get('audioFormat') == 1)
  assert.ok(header.get('bitDepth') == 16)
  assert.ok(header.get('numberOfChannels') == 1)
  assert.ok(header.get('sampleRate') == 24000)
  console.log("fileSize: " + header.get('fileSize'));
  console.log("dataOffset: " + header.get('dataOffset'));
  console.log("dataSize: " + header.get('dataSize'));
  console.log("durationMs: " + header.get('durationMs'));
  console.log("durationMinutes: " + header.get('durationMinutes'));
  console.log("fileSize: " + header.get('fileSize'));
  })
//--------------------------------------------------------------------------------
test('getHeader.owlLivesThere', async () => {

  console.log("--- testing getHeader.owl");

  const url = "https://slexildata.artsrn.ualberta.ca/lushootseed/marthaLamont/owlLivesThere/owlLivesThere-mono-8k.wav"

  const clip = new RemoteWavClip(url, 0, 1000);
  const header = await clip.getHeader()
  assert.ok(header instanceof Map);
  const keys = Array.from(header.keys()).sort()
  console.log(keys);
  console.log("------ owl header");
  for(const key of keys){
    console.log(key + ": " + header.get(key))
    }
  assert.deepStrictEqual(keys, ['audioFormat', 'bitDepth',
                                'dataOffset', 'dataSize',
                                'durationMinutes', 'durationMs',
                                'fileSize',
                                'numberOfChannels', 'sampleRate'])
  assert.ok(header.get('audioFormat') == 1)
  assert.ok(header.get('bitDepth') == 16)
  assert.ok(header.get('numberOfChannels') == 1)
  assert.ok(header.get('sampleRate') == 8000)
  console.log("fileSize: " + header.get('fileSize'));
  console.log("dataOffset: " + header.get('dataOffset'));
  console.log("dataSize: " + header.get('dataSize'));
  console.log("durationMs: " + header.get('durationMs'));
  console.log("durationMinutes: " + header.get('durationMinutes'));
  
  })

//--------------------------------------------------------------------------------
test('getBlob.daylight', async () => {

  console.log("--- testing getBlob.daylight");

  const url = "https://pshannon.net/tmp/new.wav"
  var clip = new RemoteWavClip(url, 0, 1000);
  var header = await clip.getHeader()

  var blob = await clip.retrieve()
  console.log("--- blob: ")
  console.log(blob)
  assert.ok(blob['size'] == 48044)
  assert.ok(blob['type'] == 'audio/wav')

     // now get much shorter clip from later in the file
  clip = new RemoteWavClip(url, 2000, 2100);
  header = await clip.getHeader()

  blob = await clip.retrieve()
  console.log("--- small blob: ")
  console.log(blob)
  assert.ok(blob['size'] == 4844)
  assert.ok(blob['type'] == 'audio/wav')
  })

//--------------------------------------------------------------------------------
  