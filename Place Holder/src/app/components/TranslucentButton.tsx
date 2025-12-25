import { motion } from "motion/react";
import { useState } from "react";

interface TranslucentButtonProps {
  children: React.ReactNode;
  onClick?: () => void;
}

export function TranslucentButton({ children, onClick }: TranslucentButtonProps) {
  const [isPressed, setIsPressed] = useState(false);

  return (
    <motion.button
      className="relative px-8 py-4 bg-white/20 backdrop-blur-md border border-white/30 rounded-2xl overflow-hidden cursor-pointer"
      style={{
        transformStyle: "preserve-3d",
      }}
      animate={{
        scale: isPressed ? 0.95 : 1,
        y: isPressed ? 8 : 0,
      }}
      whileHover={{
        scale: 1.02,
        y: -2,
      }}
      transition={{
        type: "spring",
        stiffness: 400,
        damping: 17,
      }}
      onMouseDown={() => setIsPressed(true)}
      onMouseUp={() => setIsPressed(false)}
      onMouseLeave={() => setIsPressed(false)}
      onTouchStart={() => setIsPressed(true)}
      onTouchEnd={() => setIsPressed(false)}
      onClick={onClick}
    >
      {/* Depth shadow layers */}
      <motion.div
        className="absolute inset-0 rounded-2xl"
        style={{
          background: "linear-gradient(135deg, rgba(255,255,255,0.3) 0%, rgba(255,255,255,0.1) 100%)",
          transform: "translateZ(-1px)",
        }}
        animate={{
          opacity: isPressed ? 0.5 : 1,
        }}
      />
      
      {/* Shadow below button */}
      <motion.div
        className="absolute -bottom-2 left-1/2 -translate-x-1/2 w-[90%] h-8 rounded-full"
        style={{
          background: "radial-gradient(ellipse at center, rgba(0,0,0,0.3) 0%, rgba(0,0,0,0) 70%)",
          filter: "blur(8px)",
          zIndex: -1,
        }}
        animate={{
          opacity: isPressed ? 0.2 : 0.6,
          y: isPressed ? -6 : 0,
          scale: isPressed ? 0.8 : 1,
        }}
        transition={{
          type: "spring",
          stiffness: 400,
          damping: 17,
        }}
      />

      {/* Inner shadow when pressed */}
      <motion.div
        className="absolute inset-0 rounded-2xl pointer-events-none"
        style={{
          boxShadow: "inset 0 4px 12px rgba(0,0,0,0.2)",
        }}
        animate={{
          opacity: isPressed ? 1 : 0,
        }}
        transition={{
          duration: 0.1,
        }}
      />

      {/* Shine effect */}
      <motion.div
        className="absolute top-0 left-0 right-0 h-1/2 rounded-t-2xl pointer-events-none"
        style={{
          background: "linear-gradient(180deg, rgba(255,255,255,0.4) 0%, rgba(255,255,255,0) 100%)",
        }}
        animate={{
          opacity: isPressed ? 0.2 : 0.6,
        }}
      />

      {/* Button content */}
      <span className="relative z-10 text-white drop-shadow-lg">
        {children}
      </span>
    </motion.button>
  );
}
