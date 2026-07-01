export default function Loader({ step }) {
  const steps = [
    "Researching company...",
    "Identifying pain points...",
    "Building outreach...",
    "Creating follow-ups...",
    "Rendering campaign..."
  ];

  return (
    <div className="p-4 bg-gray-900 rounded-xl border border-gray-700">
      {steps.map((s, i) => (
        <p key={i} className={i <= step ? "text-green-400" : "text-gray-500"}>
          {i <= step ? "✓ " : "… "} {s}
        </p>
      ))}
    </div>
  );
}