import { StateGraph, END } from "langgraph";
import { BaseMessage, HumanMessage } from "@langchain/core/messages";
import { ChatOpenAI } from "@langchain/openai";

const model = new ChatOpenAI({
    temperature: 0,
    streaming: true,
});

interface AgentState {
  messages: BaseMessage[];
}

const workflow = new StateGraph<AgentState>({
  channels: {
    messages: {
      value: (x: BaseMessage[], y: BaseMessage[]) => x.concat(y),
      default: () => [],
    },
  },
});

workflow.addNode("llm", async (state: AgentState) => {
    const response = await model.invoke(state.messages);
    return { messages: [response] };
});

workflow.setEntryPoint("llm");
workflow.addEdge("llm", END);

const app = workflow.compile();

export { app };
