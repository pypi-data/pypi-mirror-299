#!/usr/bin/env python3
import houndify
import argparse
import sys
import time
import wave
import json
from threading import Thread
import random

BUFFER_SIZE = 256 * 8

#
# Simplest HoundListener; just print out what we receive.
# You can use these callbacks to interact with your UI.
#
class MyListener(houndify.HoundListener):
    def __init__(self):
        pass
    def onPartialTranscript(self, transcript):
        return
        print("Partial transcript: " + transcript)
    def onFinalResponse(self, response):
        return
        print("Final response:")
        print(json.dumps(response, indent=2, sort_keys=True, ensure_ascii=False))
    def onError(self, err):
        print("Error: " + str(err))

def check_audio_compatibility(audio):
    if audio.getsampwidth() != 2:
        print("{}: wrong sample width (must be 16-bit)".format(fname))
        sys.exit()
    if audio.getframerate() != 8000 and audio.getframerate() != 16000:
        print("{}: unsupported sampling frequency (must be either 8 or 16 khz)".format(fname))
        sys.exit()
    if audio.getnchannels() != 1:
        print("{}: must be single channel (mono)".format(fname))
        sys.exit()


def send_audio_file(audio_file, client_id, client_key, ep):
    audio = wave.open(audio_file)
    check_audio_compatibility(audio)


    request_info = {
        "Polaris": {
            "ConfidenceAdjust": 0.01,
            "EnglishMinProb":0.01,
            "RespLangMinProb":0.95,
            "PolarisOnly": True
        }
    }
    client = houndify.StreamingHoundClient(client_id, client_key, "test_user", request_info, endpoint=ep, enableVAD=True)
    client.setLocation(37.388309, -121.973968)
    client.setSampleRate(audio.getframerate())

    client.start(MyListener())
    #print("waiting")
    #time.sleep(35)
    #print("sending audio")

    while True:
        chunk_start = time.time()

        #time.sleep(random.randrange(1, 100) * 1e-3) # simulate latency
        samples = audio.readframes(BUFFER_SIZE)
        chunk_duration = float(len(samples)) / (audio.getframerate() * audio.getsampwidth())
        if len(samples) == 0: break
        if client.fill(samples): break

        # # Uncomment the line below to simulate real-time request
        try:
            time.sleep(chunk_duration - time.time() + chunk_start)
        except:
            print(f"failed sleep: cd: {chunk_duration}, tt: {time.time()}, cs: {chunk_start}")

    audio.close()
    response = client.finish() # returns either final response or error
    return response


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('AUDIO_FILE', type=str,
                        help='Audio .wav file to be sent to the server')
    parser.add_argument('--endpoint', '-e', default='https://api.houndify.com/v1/audio',
                        help="The endpoint the SDK will hit to query Houndify.")
    parser.add_argument('--client-id', '-id', required=True,
                        help="Houndify client ID")
    parser.add_argument('--client-key', '-key', required=True,
                        help="Houndify client Key")
    parser.add_argument('--sample-rate', default=16000)

    args = parser.parse_args()

    audios_16k = [
        "/disk1/jbindels/tmp/failing_audios/04bd56a7-fdb5-dedf-7454-1489296ff9bb.wav",
        "/disk1/jbindels/tmp/failing_audios/0d3ec7c9-7972-4fd1-c032-37c85db3ec8a.wav",
        "/disk1/jbindels/tmp/failing_audios/1019f57d-b3c2-43cf-94bc-6f59b9b93cbd.wav",
        "/disk1/jbindels/tmp/failing_audios/1494c025-70bc-707a-bc90-f2966db0f184.wav",
        "/disk1/jbindels/tmp/failing_audios/1e9dfc4e-0862-506f-680a-bf198fec5073.wav",
        "/disk1/jbindels/tmp/failing_audios/2573e955-7bc1-268c-e686-4170a81f03b6.wav",
        "/disk1/jbindels/tmp/failing_audios/3fa10475-699c-95fe-8180-7488a2c79143.wav",
        "/disk1/jbindels/tmp/failing_audios/4582200a-f811-adcd-fd99-86f02108d541.wav",
        "/disk1/jbindels/tmp/failing_audios/541f0277-30ab-f1a6-743f-19c249f8fd1c.wav",
        "/disk1/jbindels/tmp/failing_audios/58858147-0997-cf30-f65f-bd5aee919646.wav",
        "/disk1/jbindels/tmp/failing_audios/5b309386-af23-8775-0942-92cfe15db687.wav",
        "/disk1/jbindels/tmp/failing_audios/6715137d-c6a0-d8ec-c75f-f8ead53c3034.wav",
        "/disk1/jbindels/tmp/failing_audios/7925af96-ab99-38ca-30ec-5ba1744c154b.wav",
        "/disk1/jbindels/tmp/failing_audios/8caeb919-0568-1904-0631-78ca75800aed.wav",
        "/disk1/jbindels/tmp/failing_audios/9bff5bd2-85da-f202-1abf-81b1b969397f.wav",
        "/disk1/jbindels/tmp/failing_audios/d11c15b4-13f1-f9af-7727-7f520a4c02f6.wav",
        "/disk1/jbindels/tmp/failing_audios/d9831b9d-6dca-0c5a-75e1-122be0468c5b.wav",
        "/disk1/jbindels/tmp/failing_audios/eebf6b9b-7e89-101e-1cd3-a4bf89bc0cdd.wav"
    ]

    audios_8k = [
        "/disk1/jbindels/polaris/benchmarks/en-us/4kpar_limit20_8khz/154749.9014427.wav",
        "/disk1/jbindels/polaris/benchmarks/en-us/4kpar_limit20_8khz/2381751.9014457.wav",
        "/disk1/jbindels/polaris/benchmarks/en-us/4kpar_limit20_8khz/2382027.9014415.wav",
        "/disk1/jbindels/polaris/benchmarks/en-us/4kpar_limit20_8khz/2382221.9014483.wav",
        "/disk1/jbindels/polaris/benchmarks/en-us/4kpar_limit20_8khz/2382553.9014549.wav",
        "/disk1/jbindels/polaris/benchmarks/en-us/4kpar_limit20_8khz/2383311.9014533.wav",
        "/disk1/jbindels/polaris/benchmarks/en-us/4kpar_limit20_8khz/2383421.9014477.wav",
        "/disk1/jbindels/polaris/benchmarks/en-us/4kpar_limit20_8khz/2383817.9014407.wav",
        "/disk1/jbindels/polaris/benchmarks/en-us/4kpar_limit20_8khz/2384849.9014545.wav",
        "/disk1/jbindels/polaris/benchmarks/en-us/4kpar_limit20_8khz/2385243.9014461.wav",
        "/disk1/jbindels/polaris/benchmarks/en-us/4kpar_limit20_8khz/2386259.9014569.wav",
        "/disk1/jbindels/polaris/benchmarks/en-us/4kpar_limit20_8khz/2386817.9014539.wav",
        "/disk1/jbindels/polaris/benchmarks/en-us/4kpar_limit20_8khz/2387049.9014471.wav",
        "/disk1/jbindels/polaris/benchmarks/en-us/4kpar_limit20_8khz/2387093.9014507.wav",
        "/disk1/jbindels/polaris/benchmarks/en-us/4kpar_limit20_8khz/2387151.9014523.wav",
        "/disk1/jbindels/polaris/benchmarks/en-us/4kpar_limit20_8khz/2387343.9014421.wav",
        "/disk1/jbindels/polaris/benchmarks/en-us/4kpar_limit20_8khz/2388235.9014527.wav",
        "/disk1/jbindels/polaris/benchmarks/en-us/4kpar_limit20_8khz/2388765.9014501.wav",
        "/disk1/jbindels/polaris/benchmarks/en-us/4kpar_limit20_8khz/2389113.9014495.wav",
        "/disk1/jbindels/polaris/benchmarks/en-us/4kpar_limit20_8khz/2389415.9014445.wav"
    ]

    def f():
        query_ids = set()
        print(args.sample_rate)
        audios = audios_16k if args.sample_rate == 16000 else audios_8k
        audios = audios_16k[1:]
        print(audios[0])
        for _ in range(10):
            for a in audios:
                response = send_audio_file(a, args.client_id, args.client_key, args.endpoint)
                query_ids.add(response["QueryID"])
                print(response)
                #print(query_ids)
                exit(0)
                #y = response["Disambiguation"]["ChoiceData"][0]["Transcription"]
                #if y == "":
                #    print(f"{a} - {y}")
            for q in query_ids:
                with open("query_ids.txt", "a") as f:
                    f.write(f"\n{q}")

    threads = [Thread(target=f) for _ in range(1)]
    [t.start() for t in threads]
    [t.join() for t in threads]
