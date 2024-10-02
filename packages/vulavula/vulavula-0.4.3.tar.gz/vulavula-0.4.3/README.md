# vulavula
`vulavula` is a Python client SDK designed to interact with the Vulavula API. It simplifies making requests to endpoints such as transcription, file uploads, sentiment analysis, and entity recognition. The SDK also handles network communications, error handling, and response parsing, providing a friendlier interface for developers.

## Features

- Simple and intuitive API methods for:
  - Transcribing audio files
  - Uploading files
  - Entity recognition
  - Sentiment analysis
  - Embeddings Search 
  - Translation
- Custom error handling
- Supports Python 3.8 and newer

## Installation

You can install the `vulavula` using pip:

```bash
pip install vulavula
```

For developers using PDM, add it directly to your project:

```bash
pdm add vulavula
```

## Usage
Here's a quick example to get you started:

```python
from vulavula import VulavulaClient

# Initialize the client with your API token
client = VulavulaClient("<INSERT_TOKEN>")

```

### Transcribe an audio file
Transcribe an audio file by specifying the file path and optionally providing a webhook URL for asynchronous result delivery:
```python
transcription_result = client.transcribe("path/to/your/audio/file.wav", webhook="<INSERT_URL>", language_code="<INSERT_CODE>",)
#language_code example 'zul' and together with webhook are optional
print("Transcription Submit Success:", transcription_result) #A success message, data is sent to webhook
```

#### Inputs:

- `file_path`: A string path to the audio file you want to transcribe.
- `webhook`: (Optional string) A URL to which the server will send a POST request with the transcription results.
- `language_code`: (Optional string) The language code for the uploaded file

### Upload a file
Upload audio file to the server and receive an upload ID:
```python
upload_result = client.upload_file('path/to/your/file')
print(upload_result)
```
#### Inputs:
- `file_path`: The path to the file you wish to upload.

### Perform sentiment analysis
Analyze the sentiment of a piece of text:
```python
sentiment_result = client.get_sentiments({'encoded_text': 'Ngijabulile!'})
print(sentiment_result)
```
#### Inputs:
- `data`: A dictionary with a key `encoded_text` that contains the text to analyze.

### Perform entity recognition on text data
Perform entity recognition to identify named entities within the text, such as people, places, and organizations.
```python
entity_result = client.get_entities({'text': 'President Ramaphosa gaan loop by Emfuleni Municipality.'})
print("Entity Recognition Output:", entity_result)
```
#### Inputs:
- `data`: A dictionary with a key `encoded_text` that contains the text for entity recognition.

### Intent Classification
Train the model with examples and classify new inputs to determine the intent behind each input sentence.
```python
classification_data = {
    "examples": [
        {"intent": "greeting", "example": "Hello!"},
        {"intent": "greeting", "example": "Hi there!"},
        {"intent": "goodbye", "example": "Goodbye!"},
        {"intent": "goodbye", "example": "See you later!"}
    ],
    "inputs": [
        "Hey, how are you?",
        "I must be going now."
    ]
}
classification_results = client.classify(classification_data)
print("Classification Results:", classification_results)
```
#### Inputs:
- `data`: A dictionary containing two keys:
  - `examples`: A list of dictionaries where each dictionary represents a training example with an `intent` and an `example` text.
  - `inputs`: A list of strings, each a new sentence to classify based on the trained model.

#### Classification Results:
- The output is a list of dictionaries, each corresponding to an input sentence.
- Each dictionary contains a list of `probabilities`, where each item is another dictionary detailing an `intent` and its associated `score` (a confidence level).


### Knowledge Base
##### Create a Knowledge Base (Search)
Create a collection of documents for search:
```python
knowledge_base_result = client.create_knowledgebase("<knowledge base name>")
print("Knowledge Base Creation Result:", knowledge_base_result)
```

#####  Get knowledgebases(Search)
```python
knowledgebases = client.get_knowledgebases()
print("Knowledge Bases:", knowledgebases)
```

#####  Delete knowledgebase (Search)
```python
delete_result = client.delete_knowledgebase("<knowledgebase id >")
print("Delete Result:", delete_result)
```

##### Create Documents (Search)
Upload a file and extract text to create documents in a collection:
```python
result = client.create_documents(
        "<document name>.pdf", 
        "<knowledgebase id >"
    )
print("Upload and Extract Result:", result)
```
##### Get uploaded Documents (Search)
```python
result = client.get_documents("<knowledgebase id>")
print(result)
```

##### Delete document  (Search)
```python
delete_result = client.delete_document("<document id>")
print("Delete Result:", delete_result)
```

##### Query (Search)
Perform a search query in a specific language:
```python
result = client.query(knowledgebase_id="2f422c4d-ed93-430a-870e-ce8245397e00",query="active learning",language="en_Us")
print(result)
```

### Translate Text
Translate text from one language to another:
```python
translation_data = {
  "input_text": "Lo musho ubhalwe ngesiZulu.",
  "source_lang": "zul_Latn",
  "target_lang": "eng_Latn"
}
translation_result = client.translate(translation_data)
print("Translation Result:", translation_result)
```

Upload a file and extract text to create documents in a collection:
### Error Handling
This section covers how to handle errors gracefully when using the Vulavula API.

#### Handling Specific Errors with VulavulaError
The `VulavulaError` is a custom exception class designed to provide detailed information about errors encountered during API interactions. It includes a human-readable message and a structured JSON object containing additional error details. <br>
Here’s an example of how to handle `VulavulaError`:
```python
try:
    entity_result = client.get_entities({'text': 'President Ramaphosa gaan loop by Emfuleni Municipality.'})
    print("Entity Recognition Output:", entity_result)
except VulavulaError as e:
    print("An error occurred:", e.message)
    if 'details' in e.error_data:
        print("Error Details:", e.error_data['details'])
    else:
        print("No additional error details are available.")
except Exception as e:
    print("An unexpected error occurred:", str(e))

```

#### General Exception Handling
While `VulavulaError` handles expected API-related errors, your application might encounter other unexpected exceptions. It's important to prepare for these to ensure your application can recover gracefully. 

Here's a general approach to handle unexpected exceptions:
```python
try:
    upload_id, response = client.transcribe()
    print("Action Succeeded:", response)
except VulavulaError as e:
    print("Handled VulavulaError:", e.message)
    if 'details' in e.error_data:
        print("Detailed Error Information:", e.error_data['details'])
except Exception as e:
    print("Unhandled Exception:", str(e))

```
 

## Documentation
For full documentation on using the VulavulaClient, visit the [official documentation](https://docs.lelapa.ai/).

