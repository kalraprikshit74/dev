import asyncio
import uuid
import time

from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI, HTTPException
import chromadb

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to your frontend URL for security
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],  # Allowed HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Initialize ChromaDB client
chroma_client = chromadb.PersistentClient(path="D:/MKR50/LEUWINT/DB")

# Create a collection
collection = chroma_client.get_or_create_collection(name="objects")


@app.post("/object/")
async def save(data: dict):
    """
    Store the received JSON data in ChromaDB.
    """
    try:
        # Convert data into a document format for ChromaDB
        doc_id = str(uuid.uuid4())
        collection.add(ids=[doc_id],
                       documents=[" "],
                       metadatas=[data])

        return {"message": "Data stored successfully", "id": doc_id}
    except Exception as e:
        return {"error": str(e)}


@app.get("/object/{doc_id}")
async def get_data(doc_id: str):
    try:
        result = collection.get(ids=[doc_id])
        if not result["metadatas"]:
            raise HTTPException(status_code=404, detail="Object not found")
        # await asyncio.sleep(20)
        return {"id": doc_id, "data": result["metadatas"][0]}
    except Exception as e:
        return {"error": str(e)}


@app.post("/search/")
async def search_data(query: dict):
    """
    Efficiently search objects by matching key-value pairs using ChromaDB's built-in query function.
    """
    try:
        # Query ChromaDB directly with metadata filtering
        result = collection.query(
            query_texts=[" "],  # Dummy query (since we're using metadata search)
            where=query,  # Filters only relevant objects
            n_results=10  # Limit results for efficiency
        )

        # Format the response
        matching_docs = [
            {"id": result["ids"][0][i], "data": result["metadatas"][0][i]}
            for i in range(len(result["ids"][0]))
        ]
        print(matching_docs)
        return {"matching_documents": matching_docs}
    except Exception as e:
        return {"error": str(e)}

@app.patch("/object/{doc_id}")
async def update_data(doc_id: str, updated_fields: dict):
    """
    Update an object by ID with given attributes, keeping other attributes unchanged.
    """
    try:
        # Retrieve the existing object
        result = collection.get(ids=[doc_id])

        if not result["metadatas"] or not result["metadatas"][0]:
            raise HTTPException(status_code=404, detail="object not found")

        # Merge existing data with updated fields
        existing_data = result["metadatas"][0]
        existing_data.update(updated_fields)

        # Update the object in ChromaDB
        collection.update(
            ids=[doc_id],
            metadatas=[existing_data]  # Only update metadata (JSON data)
        )

        return {"message": "object updated successfully", "id": doc_id, "updated_data": existing_data}
    except Exception as e:
        return {"error": str(e)}

@app.delete("/object/{doc_id}")
async def delete_data(doc_id: str):
    """
    Delete a specific document by its UUID.
    """
    try:
        # Check if the document exists before attempting deletion
        result = collection.get(ids=[doc_id])

        if not result["metadatas"] or not result["metadatas"][0]:
            raise HTTPException(status_code=404, detail="object not found")

        # Delete the document
        collection.delete(ids=[doc_id])

        return {"message": "object deleted successfully", "id": doc_id}
    except Exception as e:
        return {"error": str(e)}



collection = chroma_client.get_or_create_collection(name="relationship")


@app.post("/relationship/")
async def save(data: dict):
    """
    Store the received JSON data in ChromaDB.
    """
    try:
        # Convert data into a document format for ChromaDB
        doc_id = str(uuid.uuid4())
        collection.add(ids=[doc_id],
                       documents=[" "],
                       metadatas=[data])

        return {"message": "relationship stored successfully", "id": doc_id}
    except Exception as e:
        return {"error": str(e)}


@app.get("/relationship/{doc_id}")
async def get_data(doc_id: str):
    try:
        result = collection.get(ids=[doc_id])
        if not result["metadatas"]:
            raise HTTPException(status_code=404, detail="relationship not found")
        return {"id": doc_id, "data": result["metadatas"][0]}
    except Exception as e:
        return {"error": str(e)}


@app.post("/search/")
async def search_data(query: dict):
    """
    Efficiently search objects by matching key-value pairs using ChromaDB's built-in query function.
    """
    required_keys = {"fromid", "toid"}
    if not required_keys.issubset(query.keys()):
        raise HTTPException(status_code=400, detail=f"Missing required keys: {required_keys - query.keys()}")

    try:
        # Query ChromaDB directly with metadata filtering
        result = collection.query(
            query_texts=[" "],  # Dummy query (since we're using metadata search)
            where=query,  # Filters only relevant objects
            n_results=10  # Limit results for efficiency
        )

        # Format the response
        matching_docs = [
            {"id": result["ids"][0][i], "data": result["metadatas"][0][i]}
            for i in range(len(result["ids"][0]))
        ]

        return {"matching_documents": matching_docs}
    except Exception as e:
        return {"error": str(e)}

@app.patch("/relationship/{doc_id}")
async def update_data(doc_id: str, updated_fields: dict):
    """
    Update an object by ID with given attributes, keeping other attributes unchanged.
    """
    required_keys = {"fromid", "toid"}
    if not required_keys.issubset(query.keys()):
        raise HTTPException(status_code=400, detail=f"Missing required keys: {required_keys - query.keys()}")


    try:
        # Retrieve the existing object
        result = collection.get(ids=[doc_id])

        if not result["metadatas"] or not result["metadatas"][0]:
            raise HTTPException(status_code=404, detail="relationship not found")

        # Merge existing data with updated fields
        existing_data = result["metadatas"][0]
        existing_data.update(updated_fields)

        # Update the object in ChromaDB
        collection.update(
            ids=[doc_id],
            metadatas=[existing_data]  # Only update metadata (JSON data)
        )

        return {"message": "relationship updated successfully", "id": doc_id, "updated_data": existing_data}
    except Exception as e:
        return {"error": str(e)}

@app.delete("/relationship/{doc_id}")
async def delete_data(doc_id: str):
    """
    Delete a specific document by its UUID.
    """
    try:
        # Check if the document exists before attempting deletion
        result = collection.get(ids=[doc_id])

        if not result["metadatas"] or not result["metadatas"][0]:
            raise HTTPException(status_code=404, detail="relationship not found")

        # Delete the document
        collection.delete(ids=[doc_id])

        return {"message": "relationship deleted successfully", "id": doc_id}
    except Exception as e:
        return {"error": str(e)}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
