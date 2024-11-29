import { motion } from 'framer-motion';
import { cn } from '../lib/utils';

interface C3POAvatarProps {
  isListening?: boolean;
  isThinking?: boolean;
  className?: string;
}

export function C3POAvatar({ isListening, isThinking, className }: C3POAvatarProps) {
  return (
    <div className={cn("relative", className)}>
      <motion.div
        initial={{ scale: 1 }}
        animate={{
          scale: isListening ? [1, 1.1, 1] : 1,
          opacity: isThinking ? [1, 0.7, 1] : 1
        }}
        transition={{
          duration: 1.5,
          repeat: Infinity,
          ease: "easeInOut"
        }}
        className="w-32 h-32 rounded-full bg-primary flex items-center justify-center shadow-lg"
      >
        <div className="w-24 h-24 rounded-full bg-primary-dark flex items-center justify-center">
          <div className="w-16 h-16 rounded-full bg-primary-light flex items-center justify-center">
            <div className="text-4xl font-bold text-secondary">C3PO</div>
          </div>
        </div>
      </motion.div>
      
      {/* Listening indicator */}
      {isListening && (
        <motion.div
          initial={{ scale: 0.8, opacity: 0 }}
          animate={{ scale: [1, 1.2, 1], opacity: 1 }}
          transition={{ duration: 1, repeat: Infinity }}
          className="absolute -bottom-2 left-1/2 transform -translate-x-1/2"
        >
          <div className="px-4 py-1 bg-primary-dark rounded-full text-white text-sm">
            Ouvindo...
          </div>
        </motion.div>
      )}

      {/* Thinking indicator */}
      {isThinking && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="absolute -bottom-2 left-1/2 transform -translate-x-1/2"
        >
          <div className="px-4 py-1 bg-secondary rounded-full text-white text-sm">
            Pensando...
          </div>
        </motion.div>
      )}
    </div>
  );
}
