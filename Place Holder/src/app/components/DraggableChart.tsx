import { useDrag, useDrop } from "react-dnd";
import { useRef } from "react";

interface DraggableChartProps {
  id: string;
  index: number;
  children: React.ReactNode;
  moveChart: (dragIndex: number, hoverIndex: number) => void;
}

const ITEM_TYPE = "CHART";

export function DraggableChart({ id, index, children, moveChart }: DraggableChartProps) {
  const ref = useRef<HTMLDivElement>(null);

  const [{ isDragging }, drag] = useDrag({
    type: ITEM_TYPE,
    item: { id, index },
    collect: (monitor) => ({
      isDragging: monitor.isDragging(),
    }),
  });

  const [, drop] = useDrop({
    accept: ITEM_TYPE,
    hover: (item: { id: string; index: number }) => {
      if (!ref.current) {
        return;
      }
      const dragIndex = item.index;
      const hoverIndex = index;

      if (dragIndex === hoverIndex) {
        return;
      }

      moveChart(dragIndex, hoverIndex);
      item.index = hoverIndex;
    },
  });

  drag(drop(ref));

  return (
    <div
      ref={ref}
      style={{
        opacity: isDragging ? 0.5 : 1,
        cursor: "move",
      }}
      className="bg-white rounded-xl shadow-lg p-6 transition-opacity"
    >
      {children}
    </div>
  );
}
