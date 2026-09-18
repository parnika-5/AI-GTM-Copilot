import { useState } from "react";
import { generateCampaign } from "./api";
import Loader from "./components/Loader";
import Card from "./components/Card";

const OUTPUT_LABELS = {
  research_summary: "Company Research",
  pain_points: "Potential Pain Points",
  buying_signals: "Potential Buying Signals",
  email: "Cold Outreach Email",
  linkedin_message: "LinkedIn Message",
  cold_call_script: "Cold Call Script",
  follow_up_1: "Follow-Up Email #1",
  follow_up_2: "Follow-Up Email #2",
};

const OUTPUT_ORDER = [
  "research_summary",
  "pain_points",
  "buying_signals",
  "email",
  "linkedin_message",
  "cold_call_script",
  "follow_up_1",
  "follow_up_2",
];

const initialForm = {
  company: "",
  website: "",
  description: "",
};

export default function App() {
  const [form, setForm] = useState(initialForm);
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);
  const [error, setError] = useState("");
  const [step, setStep] = useState(0);

  const updateField = (field, value) => {
    setForm((previous) => ({
      ...previous,
      [field]: value,
    }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!form.company.trim()) {
      setError("Please enter a company name.");
      return;
    }

    if (!form.website.trim() && !form.description.trim()) {
      setError("Please enter a website or company description.");
      return;
    }

    setLoading(true);
    setData(null);
    setError("");
    setStep(0);

    const interval = setInterval(() => {
      setStep((current) => Math.min(current + 1, 4));
    }, 700);

    try {
      const result = await generateCampaign({
        company: form.company.trim(),
        website: form.website.trim(),
        description: form.description.trim(),
      });

      setData(result);
    } catch (err) {
      setError(
        err.message ||
          "Unable to generate the campaign. Please try again."
      );
    } finally {
      clearInterval(interval);
      setStep(4);
      setLoading(false);
    }
  };

  const formatContent = (content) => {
    if (Array.isArray(content)) {
      return content.map((item) => `• ${item}`).join("\n");
    }

    if (typeof content === "string") {
      return content;
    }

    if (content == null) {
      return "";
    }

    return JSON.stringify(content, null, 2);
  };

  const copyAllResults = async () => {
    if (!data) return;

    const text = OUTPUT_ORDER.filter(
      (key) => data[key] !== undefined
    )
      .map((key) => {
        const title = OUTPUT_LABELS[key] || key;
        return `${title}\n\n${formatContent(data[key])}`;
      })
      .join("\n\n--------------------\n\n");

    try {
      await navigator.clipboard.writeText(text);
      alert("Campaign copied to clipboard!");
    } catch {
      alert("Unable to copy automatically. Please try again.");
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      <div className="max-w-5xl mx-auto px-6 py-12">
        {/* Header */}
        <header className="mb-10">
          <div className="inline-flex items-center px-3 py-1 mb-4 rounded-full bg-blue-500/10 border border-blue-500/30 text-blue-300 text-sm">
            AI-Powered Sales Intelligence
          </div>

          <h1 className="text-4xl md:text-5xl font-bold tracking-tight mb-4">
            AI GTM <span className="text-blue-400">Copilot</span>
          </h1>

          <p className="text-slate-400 text-lg max-w-2xl">
            Transform company information into actionable sales insights,
            personalized outreach, and a complete outbound campaign.
          </p>
        </header>

        {/* Input Form */}
        <section className="bg-slate-900 border border-slate-800 rounded-2xl p-6 md:p-8 shadow-xl">
          <div className="mb-6">
            <h2 className="text-xl font-semibold mb-2">
              Research a Prospect
            </h2>

            <p className="text-sm text-slate-400">
              Enter company information to generate a personalized
              go-to-market campaign.
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-5">
            <div>
              <label
                htmlFor="company"
                className="block text-sm font-medium text-slate-300 mb-2"
              >
                Company Name *
              </label>

              <input
                id="company"
                type="text"
                value={form.company}
                onChange={(event) =>
                  updateField("company", event.target.value)
                }
                placeholder="e.g., Acme AI"
                required
                disabled={loading}
                className="w-full px-4 py-3 bg-slate-950 border border-slate-700 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-60"
              />
            </div>

            <div>
              <label
                htmlFor="website"
                className="block text-sm font-medium text-slate-300 mb-2"
              >
                Company Website
              </label>

              <input
                id="website"
                type="text"
                value={form.website}
                onChange={(event) =>
                  updateField("website", event.target.value)
                }
                placeholder="https://example.com"
                disabled={loading}
                className="w-full px-4 py-3 bg-slate-950 border border-slate-700 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-60"
              />
            </div>

            <div>
              <label
                htmlFor="description"
                className="block text-sm font-medium text-slate-300 mb-2"
              >
                Company Description
              </label>

              <textarea
                id="description"
                value={form.description}
                onChange={(event) =>
                  updateField("description", event.target.value)
                }
                placeholder="What does the company do? What products or services does it offer?"
                rows={5}
                disabled={loading}
                className="w-full px-4 py-3 bg-slate-950 border border-slate-700 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-60 resize-y"
              />
            </div>

            <p className="text-xs text-slate-500">
              Provide a website or description. The app does not
              automatically browse websites. Verify AI-generated
              information before using it in outreach.
            </p>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 px-6 bg-blue-600 hover:bg-blue-500 disabled:bg-blue-900 disabled:cursor-not-allowed rounded-lg font-semibold transition-colors"
            >
              {loading ? "Generating Campaign..." : "Generate Campaign →"}
            </button>
          </form>
        </section>

        {/* Loading */}
        {loading && (
          <div className="mt-8 bg-slate-900 border border-slate-800 rounded-xl p-6">
            <Loader step={step} />
            <p className="text-sm text-slate-400 mt-3">
              Analyzing the provided information and generating your
              outbound campaign...
            </p>
          </div>
        )}

        {/* Error */}
        {error && (
          <div
            role="alert"
            className="mt-8 p-4 bg-red-950/60 border border-red-700 rounded-xl text-red-200"
          >
            <p className="font-semibold mb-1">Something went wrong</p>
            <p className="text-sm">{error}</p>
          </div>
        )}

        {/* Results */}
        {data && (
          <section className="mt-12">
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
              <div>
                <h2 className="text-2xl font-bold">
                  Your GTM Campaign
                </h2>

                <p className="text-slate-400 text-sm mt-1">
                  Generated for {form.company}
                </p>
              </div>

              <button
                type="button"
                onClick={copyAllResults}
                className="px-4 py-2 bg-slate-800 hover:bg-slate-700 border border-slate-700 rounded-lg text-sm font-medium transition-colors"
              >
                Copy All Results
              </button>
            </div>

            <div className="space-y-5">
              {OUTPUT_ORDER.filter(
                (key) => data[key] !== undefined
              ).map((key) => (
                <Card
                  key={key}
                  title={OUTPUT_LABELS[key] || key}
                  content={formatContent(data[key])}
                />
              ))}
            </div>

            <div className="mt-8 p-4 bg-amber-500/10 border border-amber-500/30 rounded-xl">
              <p className="text-amber-200 text-sm">
                <strong>AI-generated content:</strong> Pain points,
                buying signals, and company information may contain
                hypotheses. Verify all claims before contacting
                prospects.
              </p>
            </div>
          </section>
        )}

        {/* Footer */}
        <footer className="mt-16 pt-6 border-t border-slate-800 text-center text-sm text-slate-500">
          AI GTM Copilot · Built with React, Flask, and OpenAI
        </footer>
      </div>
    </div>
  );
}
