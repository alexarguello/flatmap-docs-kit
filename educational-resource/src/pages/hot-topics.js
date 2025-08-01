import React, { useState } from 'react';
import Link from '@docusaurus/Link';
import styles from './HotTopics.module.css';

const topics = [
  { label: 'Alt Text AI', type: 'tool', link: '/docs/placeholder' },
  { label: 'Voice Navigation', type: 'tool', link: '/docs/placeholder' },
  { label: 'Real-time Captions', type: 'tool', link: '/docs/generative-ai/inference' },
  { label: 'Screen Readers', type: 'tool', link: '/docs/placeholder' },
  { label: 'NLP Assist', type: 'concept', link: '/docs/machine-learning' },
  { label: 'Accessibility Audit', type: 'protocol', link: '/docs/placeholder' },
  { label: 'Color Contrast', type: 'concept', link: '/docs/placeholder' },
  { label: 'ARIA Roles', type: 'concept', link: '/docs/placeholder' },
  { label: 'Inclusive Design', type: 'concept', link: '/docs/placeholder' },
  { label: 'Seeing AI', type: 'tool', link: '/docs/placeholder' },
  { label: 'Otter.ai', type: 'tool', link: '/docs/placeholder' },
  { label: 'GitHub Access Tools', type: 'tool', link: '/docs/agentic-ai/agent-frameworks/adk' },
  { label: 'Accessibility Testing', type: 'protocol', link: '/docs/machine-learning' },
  { label: 'SpringAI Assistive', type: 'tool', link: '/docs/generative-ai/framework-integrations/spring-ai' },
  { label: 'LangChain4J Tools', type: 'tool', link: '/docs/generative-ai/framework-integrations/langchain4j' },
  { label: 'Smart Homes', type: 'use', link: '/docs/placeholder' },
  { label: 'Dyslexia Support', type: 'concept', link: '/docs/placeholder' },
  { label: 'Bug Bounty', type: 'protocol', link: '/docs/placeholder' },
];

export default function HotTopicsPage() {
  const [reduceMotion, setReduceMotion] = useState(false);

  return (
    <main className={styles.hotTopics} role="main" aria-label="Hot Topics in Accessibility and AI">
      <div className={styles.container}>
        <h1 className={styles.header}>
          🔥 <span className={styles.hotWord}>Hot</span> Topics in Accessibility & AI
        </h1>
        <p>Click a tag to learn more. This view is fully keyboard and screen-reader accessible.</p>

        <button
          onClick={() => setReduceMotion(prev => !prev)}
          aria-pressed={reduceMotion}
          className={styles.motionToggle}
        >
          {reduceMotion ? 'Enable Animations' : 'Reduce Motion'}
        </button>

        <ul
          className={`${styles.topicsGrid} ${reduceMotion ? styles.reduceMotion : ''}`}
          role="list"
        >
          {topics.map((topic, i) => (
            <li key={i} role="listitem">
              <Link
                to={topic.link}
                className={`${styles.topicTag} ${styles[`topic-${topic.type}`]}`}
                aria-label={`Topic: ${topic.label}, Category: ${topic.type}`}
              >
                {topic.label}
              </Link>
            </li>
          ))}
        </ul>
      </div>
      <div className={styles.legend}>
        <span className={styles.toolLegend}>🧰 Tool</span>
        <span className={styles.conceptLegend}>🎓 Concept</span>
        <span className={styles.protocolLegend}>📜 Protocol</span>
        <span className={styles.useLegend}>🏠 Use Case</span>
      </div>

    </main>
  );
}
