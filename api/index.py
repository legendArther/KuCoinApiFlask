from flask import Flask,jsonify, send_file,request
from gradio_client import Client

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/generate')
def about():
    client = Client("https://prodia-fast-stable-diffusion.hf.space/")

    text_input_1 = str(request.args.get ('prompt'))
    text_input_2 = '3d, cartoon, anime, (deformed eyes, nose, ears, nose), bad anatomy, ugly'
    debugg = str(request.args.get ('dbg'))

    # text_input_1 = "A peaceful forest scene."
    # text_input_2 = "A serene river flowing through tall trees."
    checkpoint = "absolutereality_V16.safetensors [37db0fc3]"
    sampling_steps = 10
    sampling_method = "Euler"
    cfg_scale = 5
    width = 512
    height = 512
    seed = 42

    result = client.predict(
        text_input_1,
        text_input_2,
        checkpoint,
        sampling_steps,
        sampling_method,
        cfg_scale,
        width,
        height,
        seed,
        fn_index=0,
    )
    return result

@app.route('/roop', methods = ['GET','POST'])
def roop():
    src = str(request.args.get ('source'))
    tar = str(request.args.get ('target'))
    debugg = str(request.args.get ('dbg'))
    client = Client("https://chilleverydaychill-roop.hf.space/")
    result = client.predict(
                    src,tar,
                    api_name="/predict"
    )
    image_path = result
    if debugg == "true":
        return send_file(image_path, mimetype='image/png')  # Set the appropriate mimetype
      # Assuming 'result' contains the path to the image file you want to send
    #                 return send_file(image_path, mimetype='image/png')  # Set the appropriate mimetype
    else:
        return result
    
@app.route('/test')
def tst():
    return 'testlog123'