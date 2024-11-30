'use client';

import * as React from 'react';

export function AlgorithmExplanation() {
    return (
        <div className="mt-4 p-4 bg-blue-50 rounded-lg border border-blue-100">
            <h4 className="font-medium text-blue-900 mb-3">
                Look Under the Hood: How It Actually Works
            </h4>

            {/* System Components */}
            <div className="space-y-4">
                <div>
                    <h5 className="text-sm font-medium text-blue-800 mb-2">1. Pattern Storage (MongoDB)</h5>
                    <ul className="text-sm text-blue-700 list-disc list-inside space-y-1">
                        <li>Stores the raw content of each pattern</li>
                        <li>Tracks when and how patterns change over time</li>
                        <li>Like a journal that remembers everything we learn</li>
                    </ul>
                </div>

                <div>
                    <h5 className="text-sm font-medium text-blue-800 mb-2">2. Pattern Connections (Neo4j)</h5>
                    <ul className="text-sm text-blue-700 list-disc list-inside space-y-1">
                        <li>Creates a web of connections between patterns</li>
                        <li>Like a mind map showing how ideas relate</li>
                        <li>Example: When you click a theme, it uses Neo4j to find related patterns</li>
                    </ul>
                </div>

                <div>
                    <h5 className="text-sm font-medium text-blue-800 mb-2">3. Understanding Meaning (Pinecone)</h5>
                    <ul className="text-sm text-blue-700 list-disc list-inside space-y-1">
                        <li>Understands the meaning behind patterns</li>
                        <li>Finds similar patterns even if words are different</li>
                        <li>Like having an intuition about related ideas</li>
                    </ul>
                </div>

                <div>
                    <h5 className="text-sm font-medium text-blue-800 mb-2">How They Work Together:</h5>
                    <p className="text-sm text-blue-700 mb-2">
                        When you explore a theme:
                    </p>
                    <ol className="text-sm text-blue-700 list-decimal list-inside space-y-1">
                        <li>Neo4j finds directly connected patterns</li>
                        <li>Pinecone finds semantically similar patterns</li>
                        <li>MongoDB provides the full history and evolution</li>
                        <li>All three combine to show you the complete picture</li>
                    </ol>
                </div>

                <div className="mt-3 pt-3 border-t border-blue-200">
                    <p className="text-xs text-blue-600">
                        Want to learn more? Check out our{' '}
                        <a href="https://github.com/yourusername/cognitive-agents" 
                           className="underline hover:text-blue-800">
                            open source code
                        </a>
                        {' '}to see exactly how it works.
                    </p>
                </div>
            </div>
        </div>
    );
} 