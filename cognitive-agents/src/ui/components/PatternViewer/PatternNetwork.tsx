'use client';

import * as React from 'react';
import type { Pattern } from '../../types/components';

interface PatternNetworkProps {
    pattern: Pattern;
    onExploreConnection: (connectionId: string) => void;
}

export function PatternNetwork({ pattern, onExploreConnection }: PatternNetworkProps) {
    return (
        <div className="mt-4 space-y-6">
            {/* Interactive Network Map */}
            <div className="p-4 bg-gradient-to-br from-blue-50 to-indigo-50 rounded-lg">
                <h4 className="font-medium text-blue-900 mb-4">Pattern Network</h4>
                
                {/* Strength Indicators */}
                <div className="grid grid-cols-3 gap-4 mb-6">
                    <div className="p-3 bg-white/80 rounded-lg backdrop-blur-sm">
                        <div className="text-sm text-blue-800">Connection Strength</div>
                        <div className="mt-1 flex items-end gap-1">
                            <div className="flex-grow bg-blue-100 rounded-full h-2">
                                <div className="bg-blue-500 h-2 rounded-full" style={{ width: '85%' }} />
                            </div>
                            <span className="text-xs text-blue-600">85%</span>
                        </div>
                    </div>
                    <div className="p-3 bg-white/80 rounded-lg backdrop-blur-sm">
                        <div className="text-sm text-blue-800">Growth Rate</div>
                        <div className="mt-1 flex items-end gap-1">
                            <div className="flex-grow bg-blue-100 rounded-full h-2">
                                <div className="bg-blue-500 h-2 rounded-full" style={{ width: '60%' }} />
                            </div>
                            <span className="text-xs text-blue-600">60%</span>
                        </div>
                    </div>
                    <div className="p-3 bg-white/80 rounded-lg backdrop-blur-sm">
                        <div className="text-sm text-blue-800">Stability</div>
                        <div className="mt-1 flex items-end gap-1">
                            <div className="flex-grow bg-blue-100 rounded-full h-2">
                                <div className="bg-blue-500 h-2 rounded-full" style={{ width: '75%' }} />
                            </div>
                            <span className="text-xs text-blue-600">75%</span>
                        </div>
                    </div>
                </div>

                {/* Interactive Connections */}
                <div className="space-y-3">
                    {['direct', 'emerging', 'potential'].map((type) => (
                        <button
                            key={type}
                            type="button"
                            onClick={() => onExploreConnection(type)}
                            className="w-full p-3 bg-white rounded-lg hover:bg-blue-50 
                                     transition-colors duration-200 group"
                        >
                            <div className="flex items-center justify-between">
                                <div>
                                    <h5 className="text-sm font-medium text-blue-800">
                                        {type === 'direct' ? 'Strong Connection' :
                                         type === 'emerging' ? 'Growing Connection' :
                                         'Potential Connection'}
                                    </h5>
                                    <p className="text-sm text-blue-600 mt-1">
                                        {type === 'direct' ? 'Learning through patterns' :
                                         type === 'emerging' ? 'Natural development' :
                                         'Future possibilities'}
                                    </p>
                                </div>
                                <div className="opacity-0 group-hover:opacity-100 
                                              transition-opacity duration-200">
                                    <span className="text-xs text-blue-500">
                                        Explore →
                                    </span>
                                </div>
                            </div>
                            
                            {/* Connection Visualization */}
                            <div className="mt-2 flex items-center gap-2">
                                <div className="w-2 h-2 rounded-full bg-blue-500" />
                                <div className="flex-grow h-px bg-blue-200" />
                                <div className="w-2 h-2 rounded-full bg-blue-300" />
                            </div>
                        </button>
                    ))}
                </div>
            </div>

            {/* Dynamic Insights */}
            <div className="p-4 bg-white border border-blue-100 rounded-lg">
                <h5 className="text-sm font-medium text-blue-800 mb-3">
                    Active Development
                </h5>
                <div className="space-y-2">
                    <div className="flex items-center gap-2 text-sm text-blue-600">
                        <span className="block w-2 h-2 rounded-full bg-green-400" />
                        New connection forming with "learning patterns"
                    </div>
                    <div className="flex items-center gap-2 text-sm text-blue-600">
                        <span className="block w-2 h-2 rounded-full bg-yellow-400" />
                        Growing relationship with "natural development"
                    </div>
                    <div className="flex items-center gap-2 text-sm text-blue-600">
                        <span className="block w-2 h-2 rounded-full bg-blue-400" />
                        Stable connection with "pattern recognition"
                    </div>
                </div>
            </div>
        </div>
    );
} 