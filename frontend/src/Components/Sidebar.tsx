import { MessageSquare, PlusCircle } from "lucide-react";

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

interface SidebarProps {
  chats: Chat[];
  currentChat: string;
  onNewChat: () => void;
  onSelectChat: (id: string) => void;
}

export function Sidebar({
  chats,
  currentChat,
  onNewChat,
  onSelectChat,
}: SidebarProps) {
  return (
    <div className="w-72 bg-gray-900 text-white p-4 flex flex-col h-full">
      <button
        onClick={onNewChat}
        className="w-full flex items-center gap-2 bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 rounded-xl p-3.5 mb-6 transition-all duration-200 shadow-lg hover:shadow-blue-500/25"
      >
        <PlusCircle size={20} className="text-blue-200" />
        <span className="font-medium">New Chat</span>
      </button>

      <div className="space-y-2 flex-1 overflow-y-auto custom-scrollbar">
        {chats.map((chat) => (
          <button
            key={chat.id}
            onClick={() => onSelectChat(chat.id)}
            className={`w-full flex items-center gap-3 rounded-xl p-3.5 transition-all duration-200 group hover:bg-gray-800
              ${
                currentChat === chat.id
                  ? "bg-gray-800 shadow-lg"
                  : "hover:shadow-md"
              }`}
          >
            <MessageSquare
              size={18}
              className={`${
                currentChat === chat.id ? "text-blue-400" : "text-gray-400"
              } 
                group-hover:text-blue-400 transition-colors duration-200`}
            />
            <span className="text-sm font-medium truncate">{chat.title}</span>
          </button>
        ))}
      </div>
    </div>
  );
}
