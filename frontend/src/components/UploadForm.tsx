import React, { useState } from "react";

interface UploadFormProps {
  onSubmit: (cvText: string, jdText: string) => void;
  isLoading: boolean;
}

const UploadForm: React.FC<UploadFormProps> = ({ onSubmit, isLoading }) => {
  const [cvText, setCvText] = useState("");
  const [jdText, setJdText] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (cvText.trim() && jdText.trim()) {
      onSubmit(cvText, jdText);
    }
  };

  const handleFileUpload = (
    e: React.ChangeEvent<HTMLInputElement>,
    setter: (val: string) => void
  ) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (ev) => {
        setter(ev.target?.result as string);
      };
      reader.readAsText(file);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="upload-form">
      <div className="upload-form__grid">
        <div className="upload-form__field">
          <div className="upload-form__label-row">
            <label className="upload-form__label">Your CV</label>
            <label className="upload-form__file-btn">
              Upload .txt
              <input
                type="file"
                accept=".txt"
                onChange={(e) => handleFileUpload(e, setCvText)}
                hidden
              />
            </label>
          </div>
          <textarea
            className="upload-form__textarea"
            value={cvText}
            onChange={(e) => setCvText(e.target.value)}
            placeholder="Paste your CV text here or upload a .txt file..."
            rows={14}
            required
          />
        </div>

        <div className="upload-form__field">
          <div className="upload-form__label-row">
            <label className="upload-form__label">Job Description</label>
            <label className="upload-form__file-btn">
              Upload .txt
              <input
                type="file"
                accept=".txt"
                onChange={(e) => handleFileUpload(e, setJdText)}
                hidden
              />
            </label>
          </div>
          <textarea
            className="upload-form__textarea"
            value={jdText}
            onChange={(e) => setJdText(e.target.value)}
            placeholder="Paste the job description text here or upload a .txt file..."
            rows={14}
            required
          />
        </div>
      </div>

      <button
        type="submit"
        className="upload-form__submit"
        disabled={isLoading || !cvText.trim() || !jdText.trim()}
      >
        {isLoading ? (
          <span className="upload-form__loading">
            <span className="spinner"></span>
            Analyzing — this may take a minute...
          </span>
        ) : (
          "Analyze Match"
        )}
      </button>
    </form>
  );
};

export default UploadForm;