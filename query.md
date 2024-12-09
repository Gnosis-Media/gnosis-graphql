query search {
  searchSimilarChunks(userId: "1", query: "example query", limit: 5) {
    chunkId
    contentId
    fileName
    text
    similarityScore
  }
}
