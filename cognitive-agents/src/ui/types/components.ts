// Core Types for Pattern Evolution UI
export interface Pattern {
    id: string;
    content: string;
    themes: string[];
    confidence: number;
    evolution: {
        stage: string;
        history: EvolutionStep[];
    };
    connections: Connection[];
}

export interface Theme {
    id: string;
    name: string;
    patterns: string[];
    strength: number;
}

export interface Connection {
    source: string;
    target: string;
    type: string;
    strength: number;
}

export interface Insight {
    id: string;
    content: string;
    patterns: string[];
    timestamp: string;
}

export interface EvolutionStep {
    stage: string;
    timestamp: string;
    changes: Change[];
}

export interface Change {
    type: 'creation' | 'modification' | 'connection' | 'evolution';
    description: string;
    before?: unknown;
    after?: unknown;
}
