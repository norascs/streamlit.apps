# Youtube AI Summarizer

I was frustrated with having to sign up for various AI summarization tools and finding one that fit my needs. Therefore, I created my own summarizer. This tool focuses on getting straight to the point by providing succinct summaries with clearly enumerated points.

At present, the summarizer uses the Groq API, which has a rate limit of 30,000 tokens per minute. This limitation can be problematic for long-form videos, such as podcasts, where the token count can quickly exceed this limit.

Once Groq releases their paid tier, this token limit issue will be resolved, allowing for more extensive summarization capabilities.

In the interim, I have also integrated the OpenAI API as an alternative summarization engine. 
