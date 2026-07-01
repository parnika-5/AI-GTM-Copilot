export default function Card({ title, content }) {
  return (
    <div className="bg-gray-900 border border-gray-700 rounded-xl p-4 mb-4">
      <h2 className="text-lg font-bold mb-2">{title}</h2>
      <pre className="whitespace-pre-wrap text-gray-300">{content}</pre>
    </div>
  );
}
