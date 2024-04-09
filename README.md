# Songs2Slides
Creates a lyrics slideshow from a list of songs

## Setup
1. Install python dependencies
```
python3 -m pip install -r requirements.txt
```

2. Add variables to `.env` file
```
API_URL="http://example.com/get-lyrics?title={title}&artist={artist}"
API_AUTH="Bearer secrettoken" # Optional
```

3. Run app in debug mode
```
flask --app songs2slides run --debug
```

4. Visit [localhost:5000](http://localhost:5000)
