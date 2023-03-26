from flask import Flask,   flash 
from flask import   request, redirect, render_template
 
from flask import send_file
import requests
from download_spotify import downloadTrack

app = Flask(__name__, template_folder='templates') 
app.config['SECRET_KEY'] = 'rhdj3hcuiehiqwehrcui23hquiechihrui23hrceui32hcuirhc'


# Need to get ID and SECRET to access Spotify Web API
sp_creds={'C_ID':YOUR_C_ID, 'C_SECRET':YOUR_C_SECRET}



@app.route('/', methods=['POST', 'GET'])
def homepage():
 
    if request.method == 'POST':
        url = request.form['spotifyTrackUrl']

        if 'https://open.spotify.com/track/' in url :
            if requests.get(url).status_code != 200: 
                return redirect('/') 
        else:
            return redirect('/')
         

        res=downloadTrack(sp_creds,url, 'downloads')
        
        flash(res['error']) 
          
        return redirect('/')

    return render_template('index.html')  
 

if __name__ == '__main__':
    app.run()