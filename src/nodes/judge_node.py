from src.chains.judge_chain import judge_chain
from src.chains.summarize_chain import summarize_chain
from src.state import Agentstate
from typing import List

def chunk(text:str,max_tokens:int=2000)->List[str]:
    """
    Splits text into chunks based on an approximate token count.
    """

    if not text:
        return []
    
    max_words=int(max_tokens*0.75)

    words=text.split()

    chunks=[]
    current_chunk_words=[]

    for word in words:
        current_chunk_words.append(word)
        if len(current_chunk_words)>=max_words:
            chunks.append(" ".join(current_chunk_words))
            current_chunk_words=[]

        
    if current_chunk_words:
        chunks.append(" ".join(current_chunk_words))
        
    return chunks if chunks else [text]
        
def judge(state:Agentstate):
    """
    Judges a debate using chunked summarization to stay within model token limits.

    Collects arguments from both 'for' and 'against' agents, splits long transcripts 
    into smaller chunks, summarizes each chunk using `summarize_chain`, and then passes 
    the combined summaries to `judge_chain` to generate the final verdict.

    Args:
        state (Agentstate): Contains the debate topic, arguments from both agents, 
                            and relevant metadata.

    Returns:
        dict: Partial state update with key 'final_judgement' containing the 
              LLM-generated verdict as a string.
    """

    topic=state["topic"]

    transcript_for="\n".join([f"-{arg.content}" for arg in state["arguments_for"]])
    transcript_against="\n".join([f"-{arg.content}" for arg in state["arguments_against"]])

    print("--- Chunking transcripts... ---")
    chunks_for=chunk(transcript_for)
    chunks_against=chunk(transcript_against)

    print(f"--- Summarizing {len(chunks_for)} chunks for 'FOR' side... ---")
    transcript_for_summarized=[summarize_chain.invoke({"topic":topic,"arguments":chunk}).content for chunk in chunks_for]

    print(f"--- Summarizing {len(chunks_against)} chunks for 'AGAINST' side... ---")
    transcript_against_summarized=[summarize_chain.invoke({"topic":topic,"arguments":chunk}).content for chunk in chunks_against]

    for_summary="\n".join(transcript_for_summarized)
    against_summary="\n".join(transcript_against_summarized)

    verdict=judge_chain.invoke({"topic":topic,"arguments_for":for_summary,"arguments_against":against_summary})

    final_text = verdict.content if hasattr(verdict, "content") else str(verdict)

    return {"final_judgement":final_text}