'use client';

import * as React from 'react';

export function ConnectionLines() {
    return (
        <div className="relative h-12 my-4">
            <div className="absolute inset-0 flex items-center justify-center">
                <div className="w-px h-full bg-gray-300 relative">
                    <div className="absolute top-0 -mt-1 left-1/2 transform -translate-x-1/2 
                                  w-3 h-3 rounded-full bg-indigo-500"/>
                    <div className="absolute bottom-0 -mb-1 left-1/2 transform -translate-x-1/2 
                                  w-3 h-3 rounded-full bg-blue-500"/>
                </div>
                <div className="absolute inset-0 flex items-center justify-center">
                    <span className="px-2 py-1 bg-white text-xs text-gray-500">
                        Connected Views
                    </span>
                </div>
            </div>
        </div>
    );
} 