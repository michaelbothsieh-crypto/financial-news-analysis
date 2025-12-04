import googlenewsdecoder
try:
    from googlenewsdecoder import new_decoderv1
    print("new_decoderv1 type:", type(new_decoderv1))
    
    url = "https://news.google.com/rss/articles/CBMiUkFVX3lxTE5hX2dIdzQtVHlUWjVYcm90MnhFOEZ1eE9DNXBjMk1LVEpRbExIVTZQLWVOVEh5WTRra1VUNzVPMExwOWNnQWZRX252eEVWcGpHZXfSAW5BVV95cUxQdnBBMmthcXZHQVRmTHhhRWpvbHA5WHlZbmZsOHRGWWZGajN5R0Rkc19IdmFCNEtEcExJUVRlNDdUNEZHRkhJLWVqSjF0RlZlRVBzRS1CaFdvZ2lXdnVwa2Vrdk95RzQ1ODJaZEMyQQ?oc=5"
    
    try:
        # Try calling it directly with URL
        res = new_decoderv1(url)
        print("Result calling with URL:", res)
    except Exception as e:
        print("Error calling with URL:", e)

    try:
        # Try calling with interval
        res = new_decoderv1(interval=0)
        print("Result calling with interval:", res)
    except Exception as e:
        print("Error calling with interval:", e)

except ImportError:
    print("Could not import new_decoderv1")
