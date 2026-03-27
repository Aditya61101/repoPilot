export interface Issue {
    id: number;
    number: number;
    title: string;
    state: string;
    createdAt: string;
    labels: string[];
    body: string;
}

export interface Repo {
    id: string;
    name: string;
}