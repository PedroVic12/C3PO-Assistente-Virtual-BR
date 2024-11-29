import { motion } from 'framer-motion';
import { cn } from '../lib/utils';

interface ChatMessageProps {
  message: string;
  isBot?: boolean;
  className?: string;
}

export function ChatMessage({ message, isBot = false, className }: ChatMessageProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className={cn(
        "flex w-full",
        isBot ? "justify-start" : "justify-end",
        className
      )}
    >
      <div
        className={cn(
          "max-w-[80%] rounded-2xl px-4 py-2",
          isBot
            ? "bg-secondary text-white rounded-tl-none"
            : "bg-primary text-secondary rounded-tr-none"
        )}
      >
        <p className="text-sm md:text-base">{message}</p>
      </div>
    </motion.div>
  );
}
