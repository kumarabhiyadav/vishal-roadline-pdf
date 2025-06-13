<template>
  <div class="invoice-list">
    <div class="app-header">
      <div class="header-content">
        <h1>Invoice Records</h1>
        <p class="header-subtitle">View and manage all generated invoices</p>
      </div>
    </div>

    <div class="controls-bar">
      <div class="search-filter-container">
        <div class="search-box">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search invoices..."
            class="search-input"
          />
          <span class="search-icon">🔍</span>
        </div>
        <div class="filter-group">
          <label>Date Range:</label>
          <input
            v-model="dateRange.start"
            type="date"
            class="date-filter"
          />
          <span>to</span>
          <input
            v-model="dateRange.end"
            type="date"
            class="date-filter"
          />
        </div>
      </div>
      <button @click="refreshData" class="refresh-btn">
        <span class="btn-icon">🔄</span>
        Refresh
      </button>
    </div>

    <div class="invoice-table-container">
      <table class="invoice-table">
        <thead>
          <tr>
            <th @click="sortBy('BillNumber')" class="sortable">
              Bill Number
              <span v-if="sortColumn === 'BillNumber'" class="sort-icon">
                {{ sortDirection === 'asc' ? '↑' : '↓' }}
              </span>
            </th>
            <th @click="sortBy('CompanyName')" class="sortable">
              Company
              <span v-if="sortColumn === 'CompanyName'" class="sort-icon">
                {{ sortDirection === 'asc' ? '↑' : '↓' }}
              </span>
            </th>
            <th @click="sortBy('InvoiceDate')" class="sortable">
              Date
              <span v-if="sortColumn === 'InvoiceDate'" class="sort-icon">
                {{ sortDirection === 'asc' ? '↑' : '↓' }}
              </span>
            </th>
            <th>Source → Destination</th>
            <th @click="sortBy('totalAmount')" class="sortable">
              Amount
              <span v-if="sortColumn === 'totalAmount'" class="sort-icon">
                {{ sortDirection === 'asc' ? '↑' : '↓' }}
              </span>
            </th>
            <th>Entries</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="invoice in filteredInvoices" :key="invoice._id">
            <td>{{ invoice.metadata.BillNumber }}</td>
            <td>{{ invoice.metadata.CompanyName }}</td>
            <td>{{ formatDate(invoice.metadata.InvoiceDate) }}</td>
            <td>
              {{ invoice.metadata.Source }} → {{ invoice.metadata.Destination }}
            </td>
            <td>₹{{ calculateTotalAmount(invoice).toLocaleString() }}</td>
            <td>{{ invoice.entries.length }}</td>
            <td class="action-buttons">
              <button @click="viewInvoice(invoice)" class="action-btn view-btn">
                View
              </button>
              <button @click="downloadInvoice(invoice)" class="action-btn download-btn">
                Download
              </button>
              <button @click="confirmDelete(invoice)" class="action-btn delete-btn">
                Delete
              </button>
            </td>
          </tr>
          <tr v-if="filteredInvoices.length === 0">
            <td colspan="7" class="no-results">No invoices found</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="pagination" v-if="filteredInvoices.length > 0">
      <button 
        @click="prevPage" 
        :disabled="currentPage === 1" 
        class="page-btn"
      >
        Previous
      </button>
      <span class="page-info">
        Page {{ currentPage }} of {{ totalPages }}
      </span>
      <button 
        @click="nextPage" 
        :disabled="currentPage === totalPages" 
        class="page-btn"
      >
        Next
      </button>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="modal-overlay">
      <div class="modal-content">
        <h3>Confirm Deletion</h3>
        <p>Are you sure you want to delete invoice {{ invoiceToDelete?.metadata?.BillNumber }}?</p>
        <div class="modal-actions">
          <button @click="showDeleteModal = false" class="modal-btn cancel-btn">
            Cancel
          </button>
          <button @click="deleteInvoice" class="modal-btn delete-btn">
            Delete
          </button>
        </div>
      </div>
    </div>

    <!-- View Invoice Dialog -->
    <div v-if="showViewDialog" class="modal-overlay">
      <div class="modal-content view-modal">
        <div class="modal-header">
          <h3>Invoice Details - {{ currentViewInvoice?.metadata?.BillNumber }}</h3>
          <button @click="showViewDialog = false" class="close-btn">&times;</button>
        </div>
        
        <div class="modal-body">
          <div class="invoice-meta">
            <div class="meta-row">
              <span class="meta-label">Company:</span>
              <span class="meta-value">{{ currentViewInvoice?.metadata?.CompanyName }}</span>
            </div>
            <div class="meta-row">
              <span class="meta-label">Date:</span>
              <span class="meta-value">{{ formatDate(currentViewInvoice?.metadata?.InvoiceDate) }}</span>
            </div>
            <div class="meta-row">
              <span class="meta-label">Route:</span>
              <span class="meta-value">{{ currentViewInvoice?.metadata?.Source }} → {{ currentViewInvoice?.metadata?.Destination }}</span>
            </div>
          </div>

          <div class="entries-section">
            <h4>Entries ({{ currentViewInvoice?.entries?.length }})</h4>
            <div class="entries-list">
              <div v-for="(entry, index) in currentViewInvoice?.entries" :key="index" class="entry-item">
                <div class="entry-header">
                  <span class="entry-number">Entry {{ index + 1 }}</span>
                </div>
                <div class="entry-details">
                  <div class="detail-row">
                    <span class="detail-label">Truck No:</span>
                    <span class="detail-value">{{ entry.TruckNo }}</span>
                  </div>
                  <div class="detail-row">
                    <span class="detail-label">LR No:</span>
                    <span class="detail-value">{{ entry.LRNo }}</span>
                  </div>
                  <div class="detail-row">
                    <span class="detail-label">Date:</span>
                    <span class="detail-value">{{ formatDate(entry.Date) }}</span>
                  </div>
                  <div class="detail-row">
                    <span class="detail-label">Quantity:</span>
                    <span class="detail-value">{{ entry.Quantity }}</span>
                  </div>
                  <div class="detail-row">
                    <span class="detail-label">Particulars:</span>
                    <span class="detail-value">{{ entry.Particulars }}</span>
                  </div>
                  <div class="detail-row">
                    <span class="detail-label">Detention:</span>
                    <span class="detail-value">₹{{ entry.Detention?.toLocaleString() }}</span>
                  </div>
                  <div class="detail-row">
                    <span class="detail-label">Amount:</span>
                    <span class="detail-value">₹{{ entry.Amount?.toLocaleString() }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="invoice-totals">
            <div class="total-row">
              <span class="total-label">Total Transport:</span>
              <span class="total-value">₹{{ calculateTransportTotal(currentViewInvoice).toLocaleString() }}</span>
            </div>
            <div class="total-row">
              <span class="total-label">Total Detention:</span>
              <span class="total-value">₹{{ calculateDetentionTotal(currentViewInvoice).toLocaleString() }}</span>
            </div>
            <div class="total-row grand-total">
              <span class="total-label">Grand Total:</span>
              <span class="total-value">₹{{ calculateTotalAmount(currentViewInvoice).toLocaleString() }}</span>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button @click="downloadInvoice(currentViewInvoice)" class="modal-btn download-btn">
            Download PDF
          </button>
          <button @click="showViewDialog = false" class="modal-btn close-btn">
            Close
          </button>
        </div>
      </div>
    </div>

    <div v-if="message" class="status-message" :class="messageType">
      <div class="message-content">
        <span class="message-icon">{{ messageType === 'success' ? '✓' : '⚠' }}</span>
        <span>{{ message }}</span>
      </div>
    </div>
  </div>
</template>

<script>
import { baseURL } from './contants';

export default {
  data() {
    return {
      invoices: [],
      searchQuery: '',
      dateRange: {
        start: '',
        end: ''
      },
      sortColumn: 'InvoiceDate',
      sortDirection: 'desc',
      currentPage: 1,
      itemsPerPage: 10,
      showDeleteModal: false,
      invoiceToDelete: null,
      showViewDialog: false,
      currentViewInvoice: null,
      message: null,
      messageType: 'success',
      loading: false
    };
  },
  computed: {
    filteredInvoices() {
      let filtered = this.invoices;

      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        filtered = filtered.filter(invoice => 
          invoice.metadata.BillNumber.toLowerCase().includes(query) ||
          invoice.metadata.CompanyName.toLowerCase().includes(query) ||
          invoice.metadata.Source.toLowerCase().includes(query) ||
          invoice.metadata.Destination.toLowerCase().includes(query)
        );
      }

      if (this.dateRange.start) {
        const startDate = new Date(this.dateRange.start);
        filtered = filtered.filter(invoice => {
          const invoiceDate = new Date(invoice.metadata.InvoiceDate);
          return invoiceDate >= startDate;
        });
      }

      if (this.dateRange.end) {
        const endDate = new Date(this.dateRange.end);
        filtered = filtered.filter(invoice => {
          const invoiceDate = new Date(invoice.metadata.InvoiceDate);
          return invoiceDate <= endDate;
        });
      }

      filtered.sort((a, b) => {
        const aValue = this.getSortValue(a);
        const bValue = this.getSortValue(b);

        if (aValue < bValue) return this.sortDirection === 'asc' ? -1 : 1;
        if (aValue > bValue) return this.sortDirection === 'asc' ? 1 : -1;
        return 0;
      });

      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return filtered.slice(start, end);
    },
    totalPages() {
      return Math.ceil(this.invoices.length / this.itemsPerPage);
    }
  },
  methods: {
   async fetchInvoices() {
      this.loading = true;
      try {
        const params = new URLSearchParams({
          search: this.searchQuery,
          start_date: this.dateRange.start,
          end_date: this.dateRange.end,
          sort_by: this.sortColumn,
          sort_dir: this.sortDirection,
          page: this.currentPage,
          per_page: this.itemsPerPage
        });

        const response = await fetch(`${baseURL}/invoices?${params.toString()}`);
        if (!response.ok) throw new Error('Failed to fetch invoices');
        
        const data = await response.json();
        this.invoices = data.invoices;
        this.totalPages = data.total_pages;
      } catch (error) {
        this.showMessage(error.message, 'error');
      } finally {
        this.loading = false;
      }
    },
    calculateTotalAmount(invoice) {
      if (!invoice?.entries) return 0;
      return invoice.entries.reduce((total, entry) => {
        return total + (entry.Amount || 0);
      }, 0);
    },
    calculateTransportTotal(invoice) {
      if (!invoice?.entries) return 0;
      return invoice.entries.reduce((total, entry) => {
        return total + (entry.Amount - (entry.Detention || 0));
      }, 0);
    },
    calculateDetentionTotal(invoice) {
      if (!invoice?.entries) return 0;
      return invoice.entries.reduce((total, entry) => {
        return total + (entry.Detention || 0);
      }, 0);
    },
    getSortValue(invoice) {
      switch (this.sortColumn) {
        case 'BillNumber': return invoice.metadata.BillNumber;
        case 'CompanyName': return invoice.metadata.CompanyName;
        case 'InvoiceDate': return new Date(invoice.metadata.InvoiceDate);
        case 'totalAmount': return this.calculateTotalAmount(invoice);
        default: return '';
      }
    },
    sortBy(column) {
      if (this.sortColumn === column) {
        this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc';
      } else {
        this.sortColumn = column;
        this.sortDirection = 'asc';
      }
    },
    formatDate(dateString) {
      if (!dateString) return '';
      const options = { year: 'numeric', month: 'short', day: 'numeric' };
      return new Date(dateString).toLocaleDateString(undefined, options);
    },
    viewInvoice(invoice) {
      this.currentViewInvoice = invoice;
      this.showViewDialog = true;
    },
    async downloadInvoice(invoice) {
  this.loading = true;
  try {
    const response = await fetch(`${baseURL}/generate-invoice`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        metadata: invoice.metadata,
        entries: invoice.entries
      })
    });

    if (!response.ok) {
      throw new Error('Failed to generate invoice');
    }

    // Get the PDF blob from response
    const blob = await response.blob();
    
    // Create filename
    const totalAmount = this.calculateTotalAmount(invoice);
    const filename = `${invoice.metadata.BillNumber}.pdf`;
    
    // Create download link
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    
    // Cleanup
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
    
    this.showMessage('Invoice downloaded successfully', 'success');
  } catch (error) {
    this.showMessage(`Download failed: ${error.message}`, 'error');
  } finally {
    this.loading = false;
  }
},
    confirmDelete(invoice) {
      this.invoiceToDelete = invoice;
      this.showDeleteModal = true;
    },
    async deleteInvoice() {
      if (!this.invoiceToDelete) return;

      this.loading = true;
      try {
        const response = await fetch(
          `${baseURL}/invoices/${this.invoiceToDelete._id}`,
          { method: 'DELETE' }
        );

        if (!response.ok) throw new Error('Failed to delete invoice');

        this.showMessage('Invoice deleted successfully', 'success');
        this.fetchInvoices();
      } catch (error) {
        this.showMessage(error.message, 'error');
      } finally {
        this.loading = false;
        this.showDeleteModal = false;
        this.invoiceToDelete = null;
      }
    },
    refreshData() {
      this.fetchInvoices();
      this.showMessage('Data refreshed', 'success');
    },
    showMessage(message, type = 'success') {
      this.message = message;
      this.messageType = type;
      setTimeout(() => {
        this.message = null;
      }, 5000);
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
      }
    },
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
      }
    }
  },
  mounted() {
    this.fetchInvoices();
  }
};
</script>

<style scoped>
.invoice-list {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  background: #f8fafc;
  color: #1e293b;
}

.app-header {
  background: white;
  border-bottom: 1px solid #e2e8f0;
  padding: 1rem;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
}

.header-content h1 {
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0 0 0.25rem 0;
  color: #1e293b;
}

.header-subtitle {
  color: #64748b;
  margin: 0;
  font-size: 0.85rem;
}

.controls-bar {
  background: white;
  padding: 1rem;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

.search-filter-container {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.search-box {
  position: relative;
}

.search-input {
  padding: 0.5rem 1rem 0.5rem 2rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 0.9rem;
  width: 250px;
}

.search-icon {
  position: absolute;
  left: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  color: #64748b;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
}

.date-filter {
  padding: 0.5rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 0.9rem;
}

.refresh-btn {
  background: #f1f5f9;
  color: #475569;
  border: 1px solid #cbd5e1;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.4rem;
  transition: all 0.2s;
  font-size: 0.9rem;
}

.refresh-btn:hover {
  background: #e2e8f0;
}

.invoice-table-container {
  flex: 1;
  padding: 1rem;
  overflow-x: auto;
}

.invoice-table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
}

.invoice-table th,
.invoice-table td {
  padding: 0.75rem 1rem;
  text-align: left;
  border-bottom: 1px solid #e2e8f0;
}

.invoice-table th {
  background: #f8fafc;
  font-weight: 600;
  color: #374151;
  font-size: 0.85rem;
  text-transform: uppercase;
}

.sortable {
  cursor: pointer;
  user-select: none;
}

.sortable:hover {
  background: #f1f5f9;
}

.sort-icon {
  margin-left: 0.25rem;
}

.invoice-table tbody tr:hover {
  background: #f8fafc;
}

.no-results {
  text-align: center;
  padding: 2rem;
  color: #64748b;
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
}

.action-btn {
  padding: 0.25rem 0.5rem;
  border: none;
  border-radius: 4px;
  font-size: 0.8rem;
  cursor: pointer;
  transition: all 0.2s;
}

.view-btn {
  background: #3b82f6;
  color: white;
}

.view-btn:hover {
  background: #2563eb;
}

.download-btn {
  background: #10b981;
  color: white;
}

.download-btn:hover {
  background: #059669;
}

.delete-btn {
  background: #ef4444;
  color: white;
}

.delete-btn:hover {
  background: #dc2626;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 1rem;
  gap: 1rem;
}

.page-btn {
  padding: 0.5rem 1rem;
  background: #f1f5f9;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  cursor: pointer;
}

.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-info {
  font-size: 0.9rem;
  color: #64748b;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  max-width: 400px;
  width: 100%;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.view-modal {
  max-width: 800px;
  width: 90%;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #e2e8f0;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.25rem;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #64748b;
  padding: 0 0.5rem;
}

.close-btn:hover {
  color: #475569;
}

.modal-body {
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem;
}

.invoice-meta {
  background: #f8fafc;
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 1.5rem;
}

.meta-row {
  display: flex;
  margin-bottom: 0.5rem;
}

.meta-row:last-child {
  margin-bottom: 0;
}

.meta-label {
  font-weight: 600;
  width: 100px;
  color: #475569;
}

.meta-value {
  flex: 1;
}

.entries-section {
  margin-top: 1.5rem;
}

.entries-section h4 {
  margin: 0 0 1rem 0;
  color: #374151;
}

.entries-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.entry-item {
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  overflow: hidden;
}

.entry-header {
  background: #f1f5f9;
  padding: 0.75rem 1rem;
  font-weight: 600;
  color: #374151;
}

.entry-details {
  padding: 1rem;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 0.75rem;
}

.detail-row {
  display: flex;
  gap: 0.5rem;
}

.detail-label {
  font-weight: 500;
  color: #475569;
}

.detail-value {
  color: #1e293b;
}

.invoice-totals {
  margin-top: 1.5rem;
  padding-top: 1rem;
  border-top: 1px solid #e2e8f0;
}

.total-row {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem 0;
}

.total-label {
  font-weight: 500;
}

.total-value {
  font-weight: 600;
}

.grand-total {
  border-top: 1px dashed #cbd5e1;
  margin-top: 0.5rem;
  padding-top: 0.75rem;
  font-size: 1.1rem;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
  padding: 1rem 1.5rem;
  border-top: 1px solid #e2e8f0;
}

.modal-btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
}

.download-btn {
  background: #10b981;
  color: white;
}

.download-btn:hover {
  background: #059669;
}

.close-btn {
  background: #f1f5f9;
  color: #475569;
}

.close-btn:hover {
  background: #e2e8f0;
}

.status-message {
  position: fixed;
  bottom: 1rem;
  left: 1rem;
  right: 1rem;
  z-index: 1000;
  border-radius: 8px;
  padding: 0.8rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  animation: slideInUp 0.3s ease-out;
  max-width: 400px;
  margin: 0 auto;
}

.status-message.success {
  background: #dcfce7;
  color: #166534;
  border: 1px solid #bbf7d0;
}

.status-message.error {
  background: #fef2f2;
  color: #dc2626;
  border: 1px solid #fecaca;
}

.message-content {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 500;
  font-size: 0.9rem;
}

.message-icon {
  font-weight: bold;
}

@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(100%);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (min-width: 768px) {
  .app-header {
    padding: 1.5rem 2rem;
  }

  .header-content h1 {
    font-size: 1.875rem;
  }

  .header-subtitle {
    font-size: 0.9rem;
  }

  .controls-bar {
    padding: 1rem 2rem;
  }

  .invoice-table-container {
    padding: 1.5rem 2rem;
  }

  .status-message {
    bottom: auto;
    top: 1rem;
    right: 1rem;
    left: auto;
    animation: slideInRight 0.3s ease-out;
  }

  @keyframes slideInRight {
    from {
      opacity: 0;
      transform: translateX(100%);
    }
    to {
      opacity: 1;
      transform: translateX(0);
    }
  }
}
</style>