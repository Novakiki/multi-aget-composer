'use client';

import * as React from 'react';

interface RealWorldExampleProps {
    theme: string;
}

export function RealWorldExample({ theme }: RealWorldExampleProps) {
    return (
        <div className="mt-4 p-4 bg-green-50 rounded-lg border border-green-100">
            <h4 className="font-medium text-green-900 mb-2">Real World Application</h4>
            
            {/* Like Social Media */}
            <div className="mb-3">
                <span className="text-xs font-medium text-green-800">Think of it like:</span>
                <p className="text-sm text-green-700">
                    When you click #{theme} on Twitter, you see related posts and hashtags.
                    Here, you're seeing how AI connects related ideas and learns from them.
                </p>
            </div>

            {/* Practical Value */}
            <div className="mb-3">
                <span className="text-xs font-medium text-green-800">Why it matters:</span>
                <ul className="text-sm text-green-700 list-disc list-inside">
                    <li>See how AI thinks and makes decisions</li>
                    <li>Guide AI's learning like a study partner</li>
                    <li>Build trust through transparency</li>
                </ul>
            </div>

            {/* Real Applications */}
            <div>
                <span className="text-xs font-medium text-green-800">Used in:</span>
                <ul className="text-sm text-green-700 list-disc list-inside">
                    <li>AI-assisted learning systems</li>
                    <li>Decision-making tools</li>
                    <li>Pattern recognition systems</li>
                </ul>
            </div>
        </div>
    );
} 