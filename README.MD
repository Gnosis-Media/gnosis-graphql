# setting

pip install -r requirements.txt


export API_KEY="t.....key" <- set up on terminal on same folder

test it's saved well by executing APi_keytester.py

python app.py to run  or flask run


# example query
query search {
  searchSimilarChunks(userId: "1", query: "example query", limit: 5) {
    chunkId
    contentId
    fileName
    text
    similarityScore
  }
}
