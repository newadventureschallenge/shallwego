---
config:
  flowchart:
    curve: linear
---
graph TD;
	__start__([<p>__start__</p>]):::first
	rag_recommendation(rag_recommendation)
	trimmed_messages(trimmed_messages)
	chatbot(chatbot)
	tools(tools)
	scoring(scoring)
	__end__([<p>__end__</p>]):::last
	__start__ --> rag_recommendation;
	chatbot -. &nbsp;__end__&nbsp; .-> scoring;
	chatbot -.-> tools;
	rag_recommendation --> trimmed_messages;
	tools --> chatbot;
	trimmed_messages --> chatbot;
	scoring --> __end__;
	classDef default fill:#f2f0ff,line-height:1.2
	classDef first fill-opacity:0
	classDef last fill:#bfb6fc