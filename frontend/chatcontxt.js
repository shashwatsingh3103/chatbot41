import React, { createContext, useState, useContext } from 'react';

// Message object: { id, sender: 'user'|'ai', text, timestamp }

const ChatContext = createContext();

export const ChatProvider = ({ children }) => {
  const [messageList, setMessageList] = useState([]);
  const [loading, setLoading] = useState(false);
  const [userInput, setUserInput] = useState('');
  const [conversationSessions, setConversationSessions] = useState([]); // array of { id, name, messages }
  const [currentConversationId, setCurrentConversationId] = useState(null);

  // Add message to current session and messageList
  const addMessage = (message) => {
    setMessageList(prev => [...prev, message]);

    // Update session messages
    setConversationSessions(prev => {
      return prev.map(session => {
        if (session.id === currentConversationId) {
          return { ...session, messages: [...session.messages, message] };
        }
        return session;
      });
    });
  };

  // Load session by id
  const loadConversation = (id) => {
    const session = conversationSessions.find(s => s.id === id);
    if (session) {
      setCurrentConversationId(id);
      setMessageList(session.messages);
    }
  };

  // Create new session
  const createNewConversation = () => {
    const newId = Date.now().toString();
    const newSession = { id: newId, name: `Conversation ${conversationSessions.length + 1}`, messages: [] };
    setConversationSessions(prev => [...prev, newSession]);
    setCurrentConversationId(newId);
    setMessageList([]);
  };

  return (
    <ChatContext.Provider value={{
      messageList,
      loading,
      userInput,
      setUserInput,
      addMessage,
      conversationSessions,
      loadConversation,
      currentConversationId,
      createNewConversation,
      setLoading
    }}>
      {children}
    </ChatContext.Provider>
  );
};

export const useChat = () => useContext(ChatContext);
