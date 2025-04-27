

export default function ResultDisplay({ result }) {
  const isDiabetic = result.prediction === 'Diabetic';
  const probabilityPercent = result.probability !== null ? (result.probability * 100).toFixed(2) : 'N/A';
  const message = isDiabetic
    ? `It seems you might have a higher probability of diabetes (${probabilityPercent}%), but please don’t worry. Consider consulting your doctor for a professional evaluation and guidance.`
    : `Congratulations! You are not diabetic, and you only have a ${probabilityPercent}% chance of having diabetes.`;

  return (
    <div
      className={`mt-6 p-6 rounded-lg shadow-md border ${
        isDiabetic ? 'border-yellow-400 bg-yellow-50' : 'border-green-400 bg-green-50'
      }`}
      role="alert"
      aria-live="polite"
    >
      <div className="flex items-center gap-3">
        <span className="text-2xl" aria-hidden="true">
          {isDiabetic ? '⚠️' : '✅'}
        </span>
        <h2 className="text-xl text-black font-semibold">Prediction Result</h2>
      </div>
      <p className="text-black mt-2">{message}</p>
      {isDiabetic && (
        <p className="mt-3">
          <a
            href="https://www.mayoclinic.org/diseases-conditions/diabetes/symptoms-causes/syc-20371444"
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-600 hover:underline"
            aria-label="Learn more about diabetes"
          >
            Learn More About Diabetes
          </a>
        </p>
      )}
    </div>
  );
}