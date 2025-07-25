import { api } from './api.js';

class CategoryApiService {
  // Helper method to handle errors
  handleError(error) {
    const message = error.response?.data?.error || 
                   error.response?.data?.message || 
                   error.message || 
                   'An unexpected error occurred';
    throw new Error(message);
  }

  // ================ CORE CATEGORY METHODS ================
  
  /**
   * Get all categories with sales data
   * @param {Object} params - Query parameters (include_deleted, etc.)
   * @returns {Promise<Object>} Categories list with sales data
   */
  async CategoryData(params = {}) {
    try {
        console.log("This API call is getting all Category");
        const response = await api.get('/category/dataview', { params });
        return response.data;
    } catch (error) {
        console.error("Error fetching all category data:", error);
        throw error;
    }
  }

  /**
   * Add new category
   * @param {Object} params - Category data
   * @returns {Promise<Object>} Created category
   */
  async AddCategoryData(params = {}) {
      try {
          console.log(`This API call is making a new category called ${params.category_name}`);
          
          const categoryData = {
              category_name: params.category_name,
              description: params.description || '',
              status: params.status || 'active',
              sub_categories: params.sub_categories || []
          };
          
          // ADD IMAGE FIELDS if they exist
          if (params.image_url) {
              categoryData.image_url = params.image_url;
              categoryData.image_filename = params.image_filename;
              categoryData.image_size = params.image_size;
              categoryData.image_type = params.image_type;
              categoryData.image_uploaded_at = params.image_uploaded_at;
          }
          
          console.log('Sending category data:', categoryData);
          const response = await api.post('/category/', categoryData);
          
          console.log('Category created successfully:', response.data);
          return response.data;
          
      } catch (error) {
          console.error(`Error creating category ${params.category_name}:`, error);
          throw error;
      }
  }

  /**
   * Update an existing category
   * @param {Object} params - Parameters including id and update data
   * @returns {Promise<Object>} Updated category data
   */
  async UpdateCategoryData(params = {}) {
      try {
          console.log(`This API call is updating category ${params.id}`);
          
          const updateData = {
              category_name: params.category_name,
              description: params.description || '',
              status: params.status || 'active',
              sub_categories: params.sub_categories || []
          };
          
          // ADD IMAGE FIELDS if they exist
          if (params.image_url) {
              updateData.image_url = params.image_url;
              updateData.image_filename = params.image_filename;
              updateData.image_size = params.image_size;
              updateData.image_type = params.image_type;
              updateData.image_uploaded_at = params.image_uploaded_at;
          }
          // Handle image removal (when user removes image)
          else if (params.image_url === null || params.image_url === '') {
              updateData.image_url = null;
              updateData.image_filename = null;
              updateData.image_size = null;
              updateData.image_type = null;
              updateData.image_uploaded_at = null;
          }
          
          // Remove undefined values
          Object.keys(updateData).forEach(key => {
              if (updateData[key] === undefined) {
                  delete updateData[key];
              }
          });
          
          console.log('Sending update data:', updateData);
          const response = await api.put(`/category/${params.id}/`, updateData);
          
          console.log('Category updated successfully:', response.data);
          return response.data;
          
      } catch (error) {
          console.error(`Error updating category ${params.id}:`, error);
          throw error;
      }
  }

  /**
   * Find specific category by ID
   * @param {Object} params - Parameters including id and include_deleted
   * @returns {Promise<Object>} Category data
   */
  async FindCategoryData(params = {}) {
    try {
        console.log(`This API call is getting ${params.id} Category`);
        
        const queryParams = {};
        if (params.include_deleted !== undefined) {
            queryParams.include_deleted = params.include_deleted;
        }
        
        const response = await api.get(`/category/${params.id}`, { params: queryParams });
        return response.data;
        
    } catch (error) {
        console.error(`Error fetching specific category ${params.id} data:`, error);
        throw error;
    }
  }

  /**
   * Find products under a category
   * @param {Object} params - Parameters including category id
   * @returns {Promise<Array>} List of products with subcategory info
   */
  async FindProdcategory(params = {}) {
      try {
          console.log(`This API call will fetch the products under the category`);
          const response = await api.get(`/category/${params.id}`);
          
          // Validate response structure
          if (!response.data || !response.data.category) {
              console.warn('Invalid response structure - missing category data');
              return [];
          }
          
          // Build a map of product name to subcategory info
          const productToSubcategory = {};
          const product_list = [];
          
          // Safely iterate through subcategories
          const subcategories = response.data.category.sub_categories || [];
          
          for (const subcategory of subcategories) {
              // Ensure subcategory has a valid products array
              const products = subcategory.products || [];
              
              // Check if products is an array
              if (Array.isArray(products)) {
                  for (const productName of products) {
                      if (productName) { // Ensure product name exists
                          productToSubcategory[productName] = {
                              name: subcategory.name,
                              id: subcategory._id || subcategory.name
                          };
                          product_list.push(productName);
                      }
                  }
              } else {
                  console.warn(`Subcategory "${subcategory.name}" has invalid products field:`, products);
              }
          }
          
          console.log('Product names from category:', product_list);
          console.log('Product to subcategory mapping:', productToSubcategory);
          
          // If no products found in category, return empty array
          if (product_list.length === 0) {
              console.log('No products found in category subcategories');
              return [];
          }
          
          // Get all products from the products API
          const prod_response = await api.get("/products/");
          console.log('All products from API:', prod_response.data);
          
          // Validate products response
          if (!prod_response.data || !Array.isArray(prod_response.data)) {
              console.warn('Invalid products API response');
              return [];
          }
          
          // Filter products and add subcategory information
          let complete_list = [];
          for (const product of prod_response.data) {
              // Check if this product's name exists in our category's product list
              if (product.product_name && product_list.includes(product.product_name)) {
                  // Get the subcategory info for this product
                  const subcategoryInfo = productToSubcategory[product.product_name];
                  
                  // Add the product with subcategory information
                  complete_list.push({
                      ...product,
                      subcategory: subcategoryInfo.name,
                      subcategory_name: subcategoryInfo.name,
                      subcategory_id: subcategoryInfo.id
                  });
              }
          }
          
          console.log('Filtered products with subcategory info:', complete_list);
          return complete_list;
          
      } catch (error) {
          console.error(`Error fetching Product List`, error);
          // Return empty array instead of throwing error to prevent UI breaking
          return [];
      }
  }

  // ================ SUBCATEGORY MANAGEMENT ================

  /**
   * Add a new subcategory to a category
   * @param {string} categoryId - Category ID
   * @param {Object} subcategoryData - Subcategory data
   * @returns {Promise<Object>} API response
   */
  async AddSubCategoryData(categoryId, subcategoryData) {
    try {
      console.log(`➕ Adding subcategory to category: ${categoryId}`);
      console.log('Subcategory data:', subcategoryData);
      
      const response = await api.post(`/category/${categoryId}/subcategories/`, {
        subcategory: subcategoryData
      });
      
      console.log('✅ Subcategory added successfully:', response.data);
      return response.data;
      
    } catch (error) {
      console.error('❌ Error adding subcategory:', error);
      this.handleError(error);
    }
  }

  /**
   * Update a product's subcategory
   * @param {Object} params - Update parameters
   * @param {string} params.product_id - Product ID to update
   * @param {string|null} params.new_subcategory - New subcategory name
   * @param {string} params.category_id - Category ID where product exists
   * @returns {Promise<Object>} Update result
   */
  async SubCatChangeTab(params = {}) {
    try {
      console.log('🔄 SubCatChangeTab: Updating product subcategory:', params);
      
      if (!params.product_id) {
        throw new Error('Product ID is required');
      }
      
      if (!params.category_id) {
        throw new Error('Category ID is required');
      }

      const payload = {
        product_id: params.product_id,
        new_subcategory: params.new_subcategory || null,
        category_id: params.category_id
      };

      const response = await api.put('/category/product/subcategory/update/', payload);

      console.log('✅ SubCatChangeTab: Subcategory update successful:', response.data);
      return response.data;

    } catch (error) {
      console.error('❌ SubCatChangeTab: Error updating product subcategory:', error);
      this.handleError(error);
    }
  }

  async CatChangeTab(params = {}) {
    try {
      console.log('🔄 CatChangeTab: Updating product category:', params);
      
      if (!params.product_id) {
        throw new Error('Product ID is required');
      }
      
      if (!params.category_id) {
        throw new Error('Category ID is required');
      }

      const payload = {
        product_id: params.product_id,
        new_category: params.category || null,
        category_id: params.category_id
      };

      const response = await api.put('category/<str:category_id>/', payload);

      console.log('✅ CatChangeTab: Category update successful:', response.data);
      return response.data;

    } catch (error) {
      console.error('❌ SubCatChangeTab: Error updating product subcategory:', error);
      this.handleError(error);
    }
  }



  // ================ DELETE METHODS ================

  /**
   * Soft delete a category
   * @param {string} categoryId - Category ID to soft delete
   * @returns {Promise<Object>} Delete result
   */
  async SoftDeleteCategory(categoryId) {
    try {
      console.log(`🗑️ Soft deleting category: ${categoryId}`);
      
      const response = await api.delete(`/category/${categoryId}/soft-delete/`);
      
      console.log('✅ Category soft deleted successfully:', response.data);
      return response.data;
      
    } catch (error) {
      console.error('❌ Error soft deleting category:', error);
      this.handleError(error);
    }
  }

  /**
   * Hard delete a category (Admin only)
   * @param {string} categoryId - Category ID to hard delete
   * @returns {Promise<Object>} Delete result
   */
  async HardDeleteCategory(categoryId) {
    try {
      console.log(`💀 Hard deleting category: ${categoryId}`);
      
      const response = await api.delete(`/category/${categoryId}/hard-delete/`);
      
      console.log('✅ Category hard deleted successfully:', response.data);
      return response.data;
      
    } catch (error) {
      console.error('❌ Error hard deleting category:', error);
      this.handleError(error);
    }
  }

  /**
   * Restore a soft-deleted category
   * @param {string} categoryId - Category ID to restore
   * @returns {Promise<Object>} Restore result
   */
  async RestoreCategory(categoryId) {
    try {
      console.log(`🔄 Restoring category: ${categoryId}`);
      
      const response = await api.post(`/category/${categoryId}/restore/`);
      
      console.log('✅ Category restored successfully:', response.data);
      return response.data;
      
    } catch (error) {
      console.error('❌ Error restoring category:', error);
      this.handleError(error);
    }
  }

  /**
   * Get category deletion impact information
   * @param {string} categoryId - Category ID to check
   * @returns {Promise<Object>} Deletion impact info
   */
  async GetCategoryDeleteInfo(categoryId) {
    try {
      console.log(`ℹ️ Getting delete info for category: ${categoryId}`);
      
      const response = await api.get(`/category/${categoryId}/delete-info/`);
      
      console.log('✅ Category delete info fetched successfully:', response.data);
      return response.data;
      
    } catch (error) {
      console.error('❌ Error fetching category delete info:', error);
      this.handleError(error);
    }
  }

  // ================ EXPORT METHODS ================

  /**
   * Export categories data
   * @param {Object} params - Export parameters (format, include_sales_data, include_deleted)
   * @returns {Promise<Blob>} Export file blob
   */
  async ExportCategoryData(params = {}) {
      try {
          console.log('🚀 Starting export with params:', params);
          
          const queryParams = {
              format: params.format || 'csv',
              include_sales_data: params.include_sales_data !== false,
              include_deleted: params.include_deleted || false
          };
          
          console.log('📤 Request params:', queryParams);
          
          const baseURL = 'http://localhost:8000/api/v1/category/exportcat/';
          
          console.log('🔍 Full URL:', baseURL);
          
          const response = await fetch(baseURL, {
              method: 'GET',
              headers: {
                  'Accept': 'text/csv, application/json, application/octet-stream, */*'
              }
          });
          
          console.log('📥 Response status:', response.status);
          
          if (!response.ok) {
              const errorText = await response.text();
              throw new Error(`HTTP ${response.status}: ${errorText}`);
          }
          
          const blob = await response.blob();
          console.log('✅ Export successful! Blob size:', blob.size);
          
          return blob;
          
      } catch (error) {
          console.error('❌ Export failed:', error);
          throw error;
      }
  }

  // ================ UTILITY METHODS ================

  /**
   * Format deletion date
   * @param {string} dateString - Date string
   * @returns {string} Formatted date
   */
  formatDeletionDate(dateString) {
    if (!dateString) return 'N/A';
    try {
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    } catch (error) {
      return 'Invalid Date';
    }
  }

   /**
   * Remove a product from current category and move to Uncategorized
   * @param {Object} params - Parameters
   * @param {string} params.product_id - Product ID to move
   * @param {string} params.current_category_id - Current category ID
   * @param {string} params.uncategorized_category_id - Uncategorized category ID
   * @returns {Promise<Object>} Move result
   */
  async MoveProductToUncategorized(params = {}) {
    try {
      console.log('🔄 Moving product to Uncategorized category:', params);
      
      if (!params.product_id) {
        throw new Error('Product ID is required');
      }

      const payload = {
        product_id: params.product_id,
        current_category_id: params.current_category_id || null
      };

      // Use the new dedicated endpoint
      const response = await api.put('/category/product/move-to-uncategorized/', payload);

      console.log('✅ Product moved to Uncategorized successfully:', response.data);
      return response.data;

    } catch (error) {
      console.error('❌ Error moving product to Uncategorized:', error);
      this.handleError(error);
    }
  }

  async UncategorizedData(params = {}) {
    try {
      console.log('🔄 Moving product to a category:', params);
      
      

      console.log('✅ Product moved to uncategorized successfully:', result);
      return result;

    } catch (error) {
      console.error('❌ Error moving product to another category:', error);
      this.handleError(error);
    }
  }

    /**
   * Move a product from current category back to Uncategorized category
   * @param {Object} params - Parameters
   * @param {string} params.product_id - Product ID to move
   * @param {string} params.current_category_id - Current category ID (optional, for logging)
   * @returns {Promise<Object>} Move result
   */
  async MoveProductToUncategorized(params = {}) {
    try {
      console.log('🔄 Moving product back to Uncategorized category:', params);
      
      if (!params.product_id) {
        throw new Error('Product ID is required');
      }

      const payload = {
        product_id: params.product_id,
        current_category_id: params.current_category_id || null,
        action: "move_to_uncategorized"
      };

      // Use a dedicated endpoint for moving to uncategorized
      const response = await api.put('/category/product/move-to-uncategorized/', payload);

      console.log('✅ Product moved to Uncategorized successfully:', response.data);
      return response.data;

    } catch (error) {
      console.error('❌ Error moving product to Uncategorized:', error);
      this.handleError(error);
    }
  }

  /**
   * Bulk move multiple products to Uncategorized category
   * @param {Object} params - Parameters
   * @param {Array} params.product_ids - Array of product IDs to move
   * @param {string} params.current_category_id - Current category ID
   * @returns {Promise<Object>} Bulk move result
   */
  async BulkMoveProductsToUncategorized(params = {}) {
    try {
      console.log('🔄 Bulk moving products to Uncategorized:', params);
      
      if (!params.product_ids || !Array.isArray(params.product_ids)) {
        throw new Error('Product IDs array is required');
      }

      const payload = {
        product_ids: params.product_ids,
        current_category_id: params.current_category_id || null
      };

      // Use the new dedicated endpoint
      const response = await api.put('/category/product/bulk-move-to-uncategorized/', payload);

      console.log('✅ Products bulk moved to Uncategorized successfully:', response.data);
      return response.data;

    } catch (error) {
      console.error('❌ Error in bulk move to Uncategorized:', error);
      this.handleError(error);
    }
  }

}

const categoryApiService = new CategoryApiService();
export default categoryApiService;

export { CategoryApiService };