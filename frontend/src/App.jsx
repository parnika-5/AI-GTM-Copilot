import { useState } from "react";
import { generateCampaign } from "./api";
import Loader from "./components/Loader";
import Card from "./components/Card";

export default function App() {
  const [form, setForm] = useState({
    company: "",
    website: "",
    description: ""
  });

  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);
  const [step, setStep] = useState(0);

  const handleSubmit = async () => {
    setLoading(true);
    setData(null);

    const interval = setInterval(() => {
      setStep((s) => (s < 4 ? s + 1 : s));
    }, 700);

    const res = await generateCampaign(form);

    clearInterval(interval);
    setStep(4);
    setData(res);
    setLoading(false);
  };

  return (
    <div className="max-w-3xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-4">AI GTM Copilot</h1>

      <input
        className="w-full p-2 mb-2 bg-gray-800 rounded"
        placeholder="Company"
        onChange={(e) => setForm({ ...form, company: e.target.value })}
      />

      <input
        className="w-full p-2 mb-2 bg-gray-800 rounded"
        placeholder="Website"
        onChange={(e) => setForm({ ...form, website: e.target.value })}
      />

      <textarea
        className="w-full p-2 mb-2 bg-gray-800 rounded"
        placeholder="Description"
        onChange={(e) => setForm({ ...form, description: e.target.value })}
      />

      <button
        className="bg-blue-600 px-4 py-2 rounded"
        onClick={handleSubmit}
      >
        Generate Campaign
      </button>

      {loading && <div className="mt-4"><Loader step={step} /></div>}

      {data && (
        <div className="mt-6">
          {Object.entries(data).map(([k, v]) => (
            <Card key={k} title={k} content={Array.isArray(v) ? v.join("\n") : v} />
          ))}
        </div>
      )}
    </div>
  );
}