import React from 'react';
import { useChat } from './ChatContext';

export default function ConversationHistoryPanel() {
  const { conversationSessions, loadConversation, currentConversationId, createNewConversation } = useChat();

  return (
    <div style={{ width: 250, borderRight: '1px solid #ccc', padding: 10 }}>
      <h3>Conversations</h3>
      <button onClick={createNewConversation}>New Conversation</button>
      <ul style={{ listStyle: 'none', padding: 0 }}>
        {conversationSessions.map(session => (
          <li
            key={session.id}
            onClick={() => loadConversation(session.id)}
            style={{
              cursor: 'pointer',
              padding: 8,
              backgroundColor: session.id === currentConversationId ? '#e0e0e0' : 'transparent'
            }}
          >
            {session.name}
          </li>
        ))}
      </ul>
    </div>
  );
}
