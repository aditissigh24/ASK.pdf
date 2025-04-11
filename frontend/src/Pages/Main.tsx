import React, { useState, useEffect } from "react";
import { Send, Upload } from "lucide-react";
import { Sidebar } from "../Components/Sidebar";

interface Chat {
  id: string;
  title: string;
  messages: Message[];
}

interface Message {
  id: string;
  content: string;
  isUser: boolean;
}

export default function Main() {
  const [chats, setChats] = useState<Chat[]>([
    { id: "1", title: "New Chat", messages: [] },
  ]);
  const [currentChat, setCurrentChat] = useState<string>("1");
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [error, setError] = useState<string | null>(null);
  // Keep a reference to the local message state
  // const pendingMessagesRef = useRef<{ [chatId: string]: Message[] }>({});

  useEffect(() => {
    console.log("Chats updated:", chats);
  }, [chats]);

  const handleNewChat = () => {
    const newChat: Chat = {
      id: Date.now().toString(),
      title: "New Chat",
      messages: [],
    };
    setChats([...chats, newChat]);
    setCurrentChat(newChat.id);
  };

  const handleSend = async () => {
    if (!input.trim()) return;
    const userInput = input.trim();
    setInput("");
    setIsTyping(true);
    setError(null);

    // Create user message
    const userMessage: Message = {
      id: `user-${Date.now().toString()}`,
      content: userInput,
      isUser: true,
    };

    // Update state with user message immediately for UI
    setChats((prevChats) => {
      return prevChats.map((chat) => {
        if (chat.id === currentChat) {
          return {
            ...chat,
            messages: [...chat.messages, userMessage],
          };
        }
        return chat;
      });
    });

    try {
      const response = await fetch(
        `https://ask-pdf-a8qa.onrender.com/ask/?question=${encodeURIComponent(
          userInput
        )}`,
        {
          method: "GET",
          mode: "cors",
        }
      );

      if (!response.ok) {
        throw new Error("Failed to get response from server");
      }

      const data = await response.json();
      console.log("API Response:", data);

      if (!data.answer || !data.answer.content) {
        throw new Error("Invalid response format");
      }

      // Create AI response message
      const aiMessage: Message = {
        id: `ai-${Date.now().toString()}`,
        content: data.answer.content,
        isUser: false,
      };

      // Update state with AI message
      setChats((prevChats) => {
        return prevChats.map((chat) => {
          if (chat.id === currentChat) {
            return {
              ...chat,
              messages: [...chat.messages, aiMessage],
            };
          }
          return chat;
        });
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
      console.error("Error:", err);
    } finally {
      setIsTyping(false);
    }
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    setIsTyping(true);
    setError(null);

    try {
      const response = await fetch(
        "https://ask-pdf-a8qa.onrender.com/upload/",
        {
          method: "POST",
          mode: "cors",
          body: formData,
        }
      );

      if (!response.ok) {
        throw new Error("Failed to upload file");
      }

      const data = await response.json();

      // Add a system message about successful upload
      setChats((prevChats) => {
        return prevChats.map((chat) => {
          if (chat.id === currentChat) {
            return {
              ...chat,
              messages: [
                ...chat.messages,
                {
                  id: Date.now().toString(),
                  content: `File "${file.name}" uploaded successfully. ${
                    data.message || ""
                  }`,
                  isUser: false,
                },
              ],
            };
          }
          return chat;
        });
      });
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "An error occurred during file upload"
      );
      console.error("Error:", err);
    } finally {
      setIsTyping(false);
      // Reset the file input
      e.target.value = "";
    }
  };

  const getCurrentChat = () => chats.find((chat) => chat.id === currentChat);

  // No more need for complex display message calculations
  const getDisplayMessages = () => {
    const chat = getCurrentChat();
    return chat ? chat.messages : [];
  };

  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar
        chats={chats}
        currentChat={currentChat}
        onNewChat={handleNewChat}
        onSelectChat={setCurrentChat}
      />

      <div className="flex-1 flex flex-col">
        {/* Messages */}
        <div className="flex-1 overflow-auto p-6 space-y-6">
          {getDisplayMessages().map((message) => (
            <div
              key={message.id}
              className={`flex ${
                message.isUser ? "justify-end" : "justify-start"
              }`}
            >
              <div
                className={`max-w-[80%] rounded-2xl p-4 shadow-sm
                  ${
                    message.isUser
                      ? "bg-gradient-to-br from-blue-500 to-blue-600 text-white"
                      : "bg-white text-gray-800 border border-gray-100"
                  }`}
              >
                <p
                  className="text-[15px] leading-relaxed"
                  style={{ whiteSpace: "pre-line" }}
                >
                  {message.content}
                </p>
              </div>
            </div>
          ))}
          {isTyping && (
            <div className="flex justify-start">
              <div className="bg-white text-gray-800 rounded-2xl p-4 shadow-sm border border-gray-100">
                <div className="flex gap-2">
                  <span className="w-2 h-2 bg-gray-300 rounded-full animate-bounce"></span>
                  <span className="w-2 h-2 bg-gray-300 rounded-full animate-bounce [animation-delay:0.2s]"></span>
                  <span className="w-2 h-2 bg-gray-300 rounded-full animate-bounce [animation-delay:0.4s]"></span>
                </div>
              </div>
            </div>
          )}
          {error && (
            <div className="flex justify-center">
              <div className="bg-red-50 text-red-600 rounded-xl p-4 shadow-sm border border-red-100">
                <p className="text-sm">{error}</p>
              </div>
            </div>
          )}
        </div>

        {/* Input Area */}
        <div className="border-t border-gray-100 p-6 bg-white">
          <div className="max-w-4xl mx-auto flex gap-4">
            <label className="flex items-center justify-center w-11 h-11 rounded-xl border border-gray-200 bg-gray-50 hover:bg-gray-200 cursor-pointer transition-colors duration-200">
              <Upload size={20} className="text-gray-600 " />
              <input
                type="file"
                className="hidden"
                accept=".pdf,.doc,.docx"
                onChange={handleFileUpload}
              />
            </label>

            <div className="flex-1 flex gap-3">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={(e) => e.key === "Enter" && handleSend()}
                placeholder="Type your message..."
                className="flex-1 rounded-xl border border-gray-200 px-4 py-3 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all duration-200"
              />
              <button
                onClick={handleSend}
                disabled={!input.trim()}
                className={`rounded-xl px-6 py-3 flex items-center gap-2 font-medium transition-all duration-200
                  ${
                    input.trim()
                      ? "bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white shadow-lg hover:shadow-blue-500/25"
                      : "bg-gray-100 text-gray-400 cursor-not-allowed"
                  }`}
              >
                <Send size={18} />
                Send
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
