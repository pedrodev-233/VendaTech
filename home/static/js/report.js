(() => {
    const status = document.getElementById('report-status');
    const refreshButton = document.getElementById('report-refresh');
    const content = document.getElementById('report-content');
    const currency = new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' });
    const number = new Intl.NumberFormat('pt-BR');
    const apiUrl = document.querySelector('meta[name="report-api"]').content;

    const setMetric = (name, value) => {
        document.querySelector(`[data-metric="${name}"]`).textContent = value;
    };

    const setCell = (row, value, className = '') => {
        const cell = document.createElement('td');
        cell.textContent = value;
        cell.className = className;
        row.appendChild(cell);
    };

    const fillTable = (bodyId, records, getCells, emptyMessage) => {
        const body = document.getElementById(bodyId);
        body.replaceChildren();
        if (records.length === 0) {
            const row = document.createElement('tr');
            const cell = document.createElement('td');
            cell.className = 'empty-row';
            cell.colSpan = body.closest('table').tHead.rows[0].cells.length;
            cell.textContent = emptyMessage;
            row.appendChild(cell);
            body.appendChild(row);
            return;
        }
        records.forEach(record => {
            const row = document.createElement('tr');
            getCells(record).forEach((value, index) => setCell(row, value, index === 0 ? 'sales-product-name' : ''));
            body.appendChild(row);
        });
    };

    const formatDate = value => {
        if (typeof value !== 'string' || !/^\d{4}-\d{2}-\d{2}$/.test(value)) {
            throw new Error('O servidor retornou uma data inválida.');
        }
        const [year, month, day] = value.split('-');
        return `${day}/${month}/${year}`;
    };

    const money = value => {
        const amount = Number(value);
        if (!Number.isFinite(amount)) throw new Error('O servidor retornou um valor financeiro inválido.');
        return currency.format(amount);
    };

    const loadReport = async () => {
        status.textContent = 'Carregando dados do relatório…';
        status.classList.remove('report-status-error');
        status.hidden = false;
        content.hidden = true;
        refreshButton.disabled = true;

        try {
            const response = await fetch(apiUrl, {
                headers: { Accept: 'application/json' },
                credentials: 'same-origin'
            });
            if (!response.ok) throw new Error(`O servidor respondeu com o status ${response.status}.`);
            const data = await response.json();
            ['products', 'results', 'employees', 'sales'].forEach(key => {
                if (!Array.isArray(data[key])) throw new Error('O servidor retornou um formato de relatório inválido.');
            });

            const productsById = new Map(data.products.map(product => [String(product.id), product]));
            const sales = data.sales.map(sale => {
                const product = productsById.get(String(sale.product));
                if (!product) throw new Error('Uma venda referencia um produto que não foi encontrado no relatório.');
                const unitValue = Number(product.value);
                const quantity = Number(sale.quantity);
                if (!Number.isFinite(unitValue) || !Number.isFinite(quantity)) {
                    throw new Error('O servidor retornou valores inválidos em uma venda.');
                }
                return { ...sale, productName: product.name, unitValue, quantity, total: unitValue * quantity };
            });

            setMetric('sales-total', money(sales.reduce((sum, sale) => sum + sale.total, 0)));
            setMetric('sales-count', number.format(sales.length));
            setMetric('units-sold', `${number.format(sales.reduce((sum, sale) => sum + sale.quantity, 0))} unidades vendidas`);
            setMetric('profit-total', money(data.results.reduce((sum, result) => sum + Number(result.profit), 0)));
            setMetric('expenses-total', `${money(data.results.reduce((sum, result) => sum + Number(result.expenses), 0))} em gastos registrados`);
            setMetric('product-count', number.format(data.products.length));

            fillTable('report-sales-body', sales, sale => [
                formatDate(sale.sale_date), sale.productName, number.format(sale.quantity),
                sale.method_of_payment, money(sale.unitValue), money(sale.total)
            ], 'Nenhuma venda registrada.');
            fillTable('report-products-body', data.products, product => [
                product.name, money(product.value)
            ], 'Nenhum produto cadastrado.');
            fillTable('report-results-body', data.results, result => {
                if (typeof result.month !== 'string' || !/^\d{4}-\d{2}-\d{2}$/.test(result.month)) {
                    throw new Error('O servidor retornou um mês inválido.');
                }
                return [
                    `${result.month.slice(5, 7)}/${result.month.slice(0, 4)}`,
                    money(result.expenses), money(result.profit)
                ];
            }, 'Nenhum resultado mensal cadastrado.');
            fillTable('report-employees-body', data.employees, employee => [
                employee.name, employee.role, money(employee.salary)
            ], 'Nenhum funcionário cadastrado.');

            const labels = { sales: 'vendas', products: 'produtos', results: 'resultados', employees: 'funcionários' };
            Object.entries(labels).forEach(([key, label]) => {
                document.querySelector(`[data-count="${key}"]`).textContent = `${number.format(data[key].length)} ${label}`;
            });

            content.hidden = false;
            status.hidden = true;
        } catch (error) {
            status.textContent = `Não foi possível carregar o relatório. ${error.message}`;
            status.classList.add('report-status-error');
        } finally {
            refreshButton.disabled = false;
        }
    };

    refreshButton.addEventListener('click', loadReport);
    loadReport();
})();
