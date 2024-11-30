'use client';

import { useState } from 'react';
import dynamic from 'next/dynamic';
import { EXAMPLE_PATTERNS } from './testData';

const PatternViewer = dynamic(
    () => import('@/components/PatternViewer').then(mod => mod.PatternViewer),
    { ssr: false }
);

export default function SandboxPage() {
    const [step, setStep] = useState(1);
    
    return (
        <div className="p-8">
            <h1 className="text-2xl font-bold mb-2">
                Pattern Learning Space
                <span className="ml-2 text-sm text-indigo-600">
                    Try It Out
                </span>
            </h1>
            
            {/* Tutorial Steps */}
            <div className="mb-8">
                <div className="flex gap-2 mb-4">
                    {[1, 2, 3].map((s) => (
                        <button
                            key={s}
                            type="button"
                            onClick={() => setStep(s)}
                            className={`px-4 py-2 rounded ${
                                step === s 
                                    ? 'bg-indigo-600 text-white' 
                                    : 'bg-gray-100'
                            }`}
                        >
                            Step {s}
                        </button>
                    ))}
                </div>
                
                <p className="text-gray-600">
                    {step === 1 ? 'Explore how patterns connect...' :
                     step === 2 ? 'See how understanding grows...' :
                     'Try creating your own patterns...'}
                </p>
            </div>

            {/* Interactive Space */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <PatternViewer pattern={EXAMPLE_PATTERNS[step - 1]} />
                
                <div className="space-y-4">
                    <div className="p-4 bg-indigo-50 rounded-lg">
                        <h3 className="font-medium text-indigo-900 mb-2">
                            Try This:
                        </h3>
                        <ul className="list-disc list-inside text-indigo-700">
                            <li>Click on different themes</li>
                            <li>Explore connections</li>
                            <li>Watch how patterns relate</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    );
} 