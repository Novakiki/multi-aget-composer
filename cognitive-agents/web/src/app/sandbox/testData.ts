import type { Pattern } from '@/types';

export const EXAMPLE_PATTERNS: Pattern[] = [
    {
        id: "example-1",
        content: "Start with a simple pattern",
        themes: ["basics", "learning", "patterns"],
        confidence: 0.7,
        evolution: {
            stage: "developing",
            history: [{
                stage: "initial",
                timestamp: "2024-01-01T00:00:00.000Z",
                changes: [{
                    type: "creation",
                    description: "First example pattern"
                }]
            }]
        },
        connections: []
    },
    {
        id: "example-2",
        content: "Watch how understanding grows",
        themes: ["understanding", "growth", "observation"],
        confidence: 0.8,
        evolution: {
            stage: "developing",
            history: [{
                stage: "initial",
                timestamp: "2024-01-01T00:00:00.000Z",
                changes: [{
                    type: "creation",
                    description: "Second example pattern"
                }]
            }]
        },
        connections: []
    },
    {
        id: "example-3",
        content: "Create your own patterns",
        themes: ["creation", "exploration", "practice"],
        confidence: 0.9,
        evolution: {
            stage: "developing",
            history: [{
                stage: "initial",
                timestamp: "2024-01-01T00:00:00.000Z",
                changes: [{
                    type: "creation",
                    description: "Third example pattern"
                }]
            }]
        },
        connections: []
    }
]; 