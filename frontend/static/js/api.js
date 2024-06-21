async function fetchProducts() {
    const response = await fetch('/api/products');
    return response.json();
}

async function addProduct(product) {
    const response = await fetch('/api/products', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(product)
    });
    return response.json();
}

async function fetchBranches() {
    const response = await fetch('/api/branches');
    return response.json();
}

async function addBranch(branch) {
    const response = await fetch('/api/branches', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(branch)
    });
    return response.json();
}
