import React from 'react';
import Link from '@docusaurus/Link';
import Layout from '@theme/Layout';
import '../css/custom.css';


const cards = [
  {
    title: 'AI for Your Domain',
    emoji: '🧩',
    headline: 'For developers in specific industries',
    description: 'Explore applications and solutions when using Java and AI in finance, healthcare, accessibility, and more.',
    link: '/docs/domain-use-cases',
    bgClass: 'card-bg-green',
  },
  {
    title: 'Full Resource Map',
    emoji: '🗺️',
    headline: 'Looking for specific topics or an overview?',
    description: 'See all the content at a glance and click to dive right into your preferred topics and tutorials.',
    link: '/docs/full-sitemap',
    bgClass: 'card-bg-blue',
  },
  {
    title: 'Frequently Asked Topics',
    emoji: '💡',
    headline: 'Want to dive into the hot topics?',
    description: 'See the most requested topics and jump directly to neural networks, RAG, chatbots, MCP, agents, and more.',
    link: '/hot-topics',
    bgClass: 'card-bg-purple',
  },
  {
    title: 'Learning Paths',
    emoji: '🧑‍🎓',
    headline: 'New to AI? Or to Java? Or to Machine Learning? ',
    description: 'Pick the curated track to get you started with Java, AI, ML, LLMs, LangChain4j, and more.',
    link: 'docs/learning-paths',
    bgClass: 'card-bg-yellow',
  },
];


export default function Home() {
  return (
    <Layout title="Java + AI Resource Hub">
      <div className="homepage">
        <main>
          <div className="homepage__container">
            <h1 className="homepage__title">Find Everything Java + AI</h1>
            <p className="homepage__subtitle">
              Explore, learn, and build across the AI landscape with Java.
            </p>

            <div className="card-grid">
              {cards.map((card, idx) => (
                <Link key={idx} to={card.link} className={`card-link ${card.bgClass}`}>
                  <h2 className="card-title">
                    <div>{card.emoji} {card.title}</div>
                  </h2>
                  <p className="card-headline">{card.headline}</p>
                  <p className="card-desc">{card.description}</p>
                  <p className="card-hover">{card.hoverText}</p>
                </Link>
              ))}
            </div>
          </div>
        </main>
      </div>
    </Layout>
  );
}
