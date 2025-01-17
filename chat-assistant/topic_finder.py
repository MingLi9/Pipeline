# import re
# from transformers import BartForConditionalGeneration, BartTokenizer, pipeline

# # Initialize the BART model and tokenizer
# model_name = "facebook/bart-large-cnn"
# tokenizer = BartTokenizer.from_pretrained(model_name)
# model = BartForConditionalGeneration.from_pretrained(model_name)

# def clean_input_text(text):
#     """
#     Cleans the input text by removing unnecessary characters.
#     """
#     # Remove special characters and numbers
#     text = re.sub(r"[^a-zA-Z\s]", "", text)
#     # Remove extra whitespace
#     text = re.sub(r"\s+", " ", text).strip()
#     return text

# def handle_short_inputs(text):
#     """
#     Handles short or vague inputs by providing additional context or rejecting them.
#     """
#     if len(text.split()) < 3:  # Less than 3 words
#         return "Input is too short. Can you provide more details?"
#     return text

# def find_topic(text):
#     """
#     Analyzes the given text and returns the topic using BART.
#     """
#     try:
#         # Pre-process the input text
#         cleaned_text = clean_input_text(text)
#         if len(cleaned_text.split()) < 3:
#             return "Too little information to determine the topic."

#         # Tokenize and summarize
#         inputs = tokenizer.encode(
#             "summarize: " + cleaned_text, 
#             return_tensors="pt", 
#             max_length=512, 
#             truncation=True
#         )
#         summary_ids = model.generate(
#             inputs, 
#             max_length=20, 
#             min_length=5, 
#             length_penalty=2.0, 
#             num_beams=4, 
#             early_stopping=True
#         )
#         topic = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
#         return topic.strip()
#     except Exception as e:
#         print(f"Error in find_topic: {e}")
#         return "Unable to determine topic. Please try again."

# # Initialize the summarization pipeline
# summarizer = pipeline("summarization", model=model_name)

# def refine_with_pipeline(text):
#     """
#     Refines the input text using a summarization pipeline.
#     """
#     try:
#         # Clean and summarize
#         cleaned_text = clean_input_text(text)
#         if len(cleaned_text.split()) < 3:
#             return "Too little information for refinement."

#         result = summarizer(
#             cleaned_text, 
#             max_length=30, 
#             min_length=10, 
#             length_penalty=2.0, 
#             num_beams=4
#         )
#         return result[0]['summary_text'].strip()
#     except Exception as e:
#         print(f"Error in pipeline processing: {e}")
#         return "Couldn't process the input. Please try again."
