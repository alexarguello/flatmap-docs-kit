import React from 'react';
import '@site/src/css/custom.css';
import Link from '@docusaurus/Link';

const topics = [
  // First line – 2 items
  { label: 'Tool calling', size: 'xl', type: 'protocol', link: '/docs/placeholder' },
  { label: 'Image recognition', size: 'lg', type: 'concept', link: '/docs/machine-learning' },

  // Line 2
  { label: 'ADK', size: 'lg', type: 'tool', link: '/docs/agentic-ai/agent-frameworks/adk' },
  { label: 'MCP', size: 'xl', type: 'protocol', link: '/docs/generative-ai/framework-integrations/mcp' },
  { label: 'Training Models', size: 'lg', type: 'concept', link: '/docs/machine-learning' },
  { label: 'Machine Learning', size: 'xl', type: 'concept', link: '/docs/machine-learning' },
  { label: 'GPU', size: 'lg', type: 'tool', link: '/docs/placeholder' },
  { label: 'Transcription', size: 'md', type: 'use', link: '/docs/placeholder' },

  // Middle line – center focus
  { label: 'LLM', size: 'xl', type: 'concept', link: '/docs/generative-ai' },
  { label: 'Finetuning', size: 'xl', type: 'concept', link: '/docs/placeholder' },
  { label: 'SpringAI', size: 'xl', type: 'tool', link: '/docs/generative-ai/framework-integrations/spring-ai' },
  { label: 'Chatbots', size: 'lg', type: 'use', link: '/docs/placeholder' },
  { label: 'Agents', size: 'lg', type: 'concept', link: '/docs/agentic-ai' },
  { label: 'OpenAI', size: 'md', type: 'tool', link: '/docs/placeholder' },

  // Line 4
  { label: 'Ollama', size: 'md', type: 'tool', link: '/docs/placeholder' },
  { label: 'Vector DBs', size: 'md', type: 'tool', link: '/docs/placeholder' },
  { label: 'Classification', size: 'md', type: 'concept', link: '/docs/machine-learning' },
  { label: 'Evaluation', size: 'md', type: 'concept', link: '/docs/machine-learning' },
  { label: 'Gemini', size: 'sm', type: 'tool', link: '/docs/placeholder' },
  { label: 'LangChain4J', size: 'lg', type: 'tool', link: '/docs/generative-ai/framework-integrations/langchain4j' },

  // Last line – 2 items
  { label: 'Hugging Face', size: 'md', type: 'tool', link: '/docs/placeholder' },
  { label: 'Local models', size: 'md', type: 'concept', link: '/docs/generative-ai/inference' },
  { label: 'Non-deterministic testing', size: 'md', type: 'concept', link: '/docs/placeholder' },
];

const HotTopicsPage = () => {
  const chunked = [];
  let index = 0;

  while (index < topics.length) {
    const count =
      index === 0 || index + 2 >= topics.length ? 2 : Math.min(6, topics.length - index);
    chunked.push(topics.slice(index, index + count));
    index += count;
  }

  return (
    <div className="hot-topics">
      <div className="hot-topics__container">
        <h1 className="hot-topics__title">Frequently Asked Topics</h1>
        <p className="hot-topics__subtitle">Explore what everyone's curious about right now, click on the topic of your choice to start reading / watching.</p>

        <div className="wordcloud">
          {chunked.map((row, i) => (
            <div key={i} className="wordcloud__row" style={{ display: 'flex', justifyContent: 'center', gap: '2rem', marginBottom: '1.5rem' }}>
              {row.map((topic, j) => (
                <Link
                  key={`${topic.label}-${j}`}
                  to={topic.link}
                  className={`word word--${topic.size} word--${topic.type} ${i % 2 === 0 ? 'rotate-left' : 'rotate-right'}`}
                >
                  {topic.label}
                </Link>
              ))}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default HotTopicsPage;
