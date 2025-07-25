from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from ..services.product_service import ProductService
import logging

# ================ PRODUCT VIEWS ================

class ProductListView(APIView):
    def get(self, request):
        """Get all products with optional filters"""
        try:
            product_service = ProductService()
            
            # Get query parameters for filtering
            filters = {}
            if request.GET.get('category_id'):
                filters['category_id'] = request.GET.get('category_id')
            if request.GET.get('status'):
                filters['status'] = request.GET.get('status')
            if request.GET.get('stock_level'):
                filters['stock_level'] = request.GET.get('stock_level')
            if request.GET.get('search'):
                filters['search'] = request.GET.get('search')
            
            include_deleted = request.GET.get('include_deleted', 'false').lower() == 'true'
            
            products = product_service.get_all_products(filters if filters else None, include_deleted)
            return Response(products, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def post(self, request):
        """Create a new product"""
        try:
            product_service = ProductService()
            product_data = request.data
            new_product = product_service.create_product(product_data)
            return Response({
                'message': 'Product created successfully', 
                'data': new_product
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )

class ProductCreateView(APIView):
    def post(self, request):
        """Create a new product (dedicated endpoint)"""
        try:
            product_service = ProductService()
            product_data = request.data
            new_product = product_service.create_product(product_data)
            return Response({
                'message': 'Product created successfully', 
                'data': new_product
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )

class ProductDetailView(APIView):
    def get(self, request, product_id):
        """Get product by ID"""
        try:
            product_service = ProductService()
            include_deleted = request.GET.get('include_deleted', 'false').lower() == 'true'
            product = product_service.get_product_by_id(product_id, include_deleted)
            if not product:
                return Response(
                    {"error": "Product not found"}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            return Response(product, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def put(self, request, product_id):
        """Update product"""
        try:
            product_service = ProductService()
            product_data = request.data
            updated_product = product_service.update_product(product_id, product_data)
            if not updated_product:
                return Response(
                    {"error": "Product not found"}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            return Response({
                'message': 'Product updated successfully', 
                'data': updated_product
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def delete(self, request, product_id):
        """Delete product (soft delete by default)"""
        try:
            product_service = ProductService()
            hard_delete = request.GET.get('hard_delete', 'false').lower() == 'true'
            deleted = product_service.delete_product(product_id, hard_delete)
            if not deleted:
                return Response(
                    {"error": "Product not found"}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            delete_type = "permanently deleted" if hard_delete else "moved to trash"
            return Response(
                {"message": f"Product {delete_type} successfully"}, 
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ProductUpdateView(APIView):
    def put(self, request, product_id):
        """Update product (dedicated endpoint)"""
        try:
            product_service = ProductService()
            product_data = request.data
            updated_product = product_service.update_product(product_id, product_data)
            if not updated_product:
                return Response(
                    {"error": "Product not found"}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            return Response({
                'message': 'Product updated successfully', 
                'data': updated_product
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def patch(self, request, product_id):
        """Partial update product"""
        return self.put(request, product_id)

class ProductDeleteView(APIView):
    def delete(self, request, product_id):
        """Delete product (dedicated endpoint)"""
        try:
            product_service = ProductService()
            hard_delete = request.GET.get('hard_delete', 'false').lower() == 'true'
            deleted = product_service.delete_product(product_id, hard_delete)
            if not deleted:
                return Response(
                    {"error": "Product not found"}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            delete_type = "permanently deleted" if hard_delete else "moved to trash"
            return Response(
                {"message": f"Product {delete_type} successfully"}, 
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ProductRestoreView(APIView):
    def post(self, request, product_id):
        """Restore a soft-deleted product"""
        try:
            product_service = ProductService()
            restored = product_service.restore_product(product_id)
            if not restored:
                return Response(
                    {"error": "Product not found or not deleted"}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            return Response(
                {"message": "Product restored successfully"}, 
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ProductBySkuView(APIView):
    def get(self, request, sku):
        """Get product by SKU"""
        try:
            product_service = ProductService()
            include_deleted = request.GET.get('include_deleted', 'false').lower() == 'true'
            product = product_service.get_product_by_sku(sku, include_deleted)
            if not product:
                return Response(
                    {"error": "Product not found"}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            return Response(product, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# ================ STOCK MANAGEMENT VIEWS ================

class ProductStockUpdateView(APIView):
    def put(self, request, product_id):
        """Update product stock with operation types"""
        try:
            product_service = ProductService()
            
            stock_data = {
                'operation_type': request.data.get('operation_type', 'set'),
                'quantity': request.data.get('quantity'),
                'reason': request.data.get('reason', 'Manual adjustment')
            }
            
            if stock_data['quantity'] is None:
                return Response(
                    {"error": "Quantity is required"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            valid_operations = ['add', 'remove', 'set']
            if stock_data['operation_type'] not in valid_operations:
                return Response(
                    {"error": f"Invalid operation_type. Must be one of: {valid_operations}"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            updated_product = product_service.update_stock(product_id, stock_data)
            
            if not updated_product:
                return Response(
                    {"error": "Product not found"}, 
                    status=status.HTTP_404_NOT_FOUND
                )
                
            return Response({
                'message': 'Stock updated successfully', 
                'data': updated_product
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def patch(self, request, product_id):
        """Alternative PATCH method for stock updates"""
        return self.put(request, product_id)

class StockAdjustmentView(APIView):
    def post(self, request, product_id):
        """Adjust stock for sales (remove stock)"""
        try:
            product_service = ProductService()
            quantity_sold = request.data.get('quantity_sold')
            
            if quantity_sold is None:
                return Response(
                    {"error": "quantity_sold is required"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            updated_product = product_service.adjust_stock_for_sale(product_id, quantity_sold)
            
            if not updated_product:
                return Response(
                    {"error": "Product not found"}, 
                    status=status.HTTP_404_NOT_FOUND
                )
                
            return Response({
                'message': 'Stock adjusted for sale successfully', 
                'data': updated_product
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )

class RestockProductView(APIView):
    def post(self, request, product_id):
        """Restock product from supplier"""
        try:
            product_service = ProductService()
            quantity_received = request.data.get('quantity_received')
            supplier_info = request.data.get('supplier_info')
            
            if quantity_received is None:
                return Response(
                    {"error": "quantity_received is required"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            updated_product = product_service.restock_product(product_id, quantity_received, supplier_info)
            
            if not updated_product:
                return Response(
                    {"error": "Product not found"}, 
                    status=status.HTTP_404_NOT_FOUND
                )
                
            return Response({
                'message': 'Product restocked successfully', 
                'data': updated_product
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )

class BulkStockUpdateView(APIView):
    def post(self, request):
        """Handle bulk stock updates for multiple products"""
        try:
            stock_updates = request.data.get('updates', [])
            
            if not stock_updates:
                return Response(
                    {'error': 'No updates provided'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            product_service = ProductService()
            results = product_service.bulk_update_stock(stock_updates)
            
            return Response({
                'message': 'Bulk stock update completed',
                'results': results
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class StockHistoryView(APIView):
    def get(self, request, product_id):
        """Get stock change history for a specific product"""
        try:
            product_service = ProductService()
            
            product = product_service.get_product_by_id(product_id)
            
            if not product:
                return Response(
                    {'error': 'Product not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Get stock history from the product's stock_history field
            stock_history = product.get('stock_history', [])
            
            # Sort by most recent first
            stock_history.sort(
                key=lambda x: x.get('timestamp', ''), 
                reverse=True
            )
            
            return Response({
                'product_id': product_id,
                'product_name': product.get('product_name'),
                'current_stock': product.get('stock'),
                'stock_history': stock_history
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# ================ PRODUCT REPORTS VIEWS ================

class LowStockProductsView(APIView):
    def get(self, request):
        """Get products with low stock"""
        try:
            product_service = ProductService()
            branch_id = request.GET.get('branch_id')
            products = product_service.get_low_stock_products(branch_id)
            return Response({
                'message': f'Found {len(products)} products with low stock',
                'data': products
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ExpiringProductsView(APIView):
    def get(self, request):
        """Get products expiring within specified days"""
        try:
            product_service = ProductService()
            days_ahead = int(request.GET.get('days_ahead', 30))
            products = product_service.get_expiring_products(days_ahead)
            return Response({
                'message': f'Found {len(products)} products expiring within {days_ahead} days',
                'data': products
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ProductsByCategoryView(APIView):
    def get(self, request, category_id):
        """Get products by category"""
        try:
            product_service = ProductService()
            products = product_service.get_products_by_category(category_id)
            return Response({
                'message': f'Found {len(products)} products in category',
                'data': products
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class DeletedProductsView(APIView):
    def get(self, request):
        """Get all soft-deleted products"""
        try:
            product_service = ProductService()
            products = product_service.get_deleted_products()
            return Response({
                'message': f'Found {len(products)} deleted products',
                'data': products
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# ================ PRODUCT SYNC VIEWS ================

class ProductSyncView(APIView):
    def post(self, request):
        """Sync products between local and cloud"""
        try:
            product_service = ProductService()
            sync_direction = request.data.get('direction', 'to_cloud')  # 'to_cloud' or 'to_local'
            
            if sync_direction == 'to_cloud':
                local_products = request.data.get('products', [])
                results = product_service.sync_from_local(local_products)
            elif sync_direction == 'to_local':
                results = product_service.sync_to_local()
            else:
                return Response(
                    {"error": "Invalid sync direction. Use 'to_cloud' or 'to_local'"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            return Response({
                'message': f'Sync {sync_direction} completed',
                'results': results
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class UnsyncedProductsView(APIView):
    def get(self, request):
        """Get products that need to be synced"""
        try:
            product_service = ProductService()
            source = request.GET.get('source', 'local')  # 'local' or 'cloud'
            products = product_service.get_unsynced_products(source)
            return Response({
                'message': f'Found {len(products)} unsynced products from {source}',
                'data': products
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class SyncStatusView(APIView):
    def get(self, request, product_id):
        """Get sync status for a product"""
        try:
            product_service = ProductService()
            product = product_service.get_product_by_id(product_id)
            
            if not product:
                return Response(
                    {"error": "Product not found"}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            sync_logs = product.get('sync_logs', [])
            return Response({
                'product_id': product_id,
                'sync_logs': sync_logs
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def put(self, request, product_id):
        """Update sync status for a product"""
        try:
            product_service = ProductService()
            sync_status = request.data.get('status', 'pending')
            source = request.data.get('source', 'cloud')
            
            success = product_service.update_sync_status(product_id, sync_status, source)
            
            if not success:
                return Response(
                    {"error": "Product not found or sync update failed"}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            return Response({
                'message': 'Sync status updated successfully'
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# ================ PRODUCT IMPORT/EXPORT VIEWS ================

class BulkCreateProductsView(APIView):
    def post(self, request):
        """Create multiple products in batch - ENHANCED WITH DEBUGGING"""
        try:
            # DEBUG: Add extensive logging
            print("=== BULK CREATE VIEW DEBUG START ===")
            print(f"Request method: {request.method}")
            print(f"Request path: {request.path}")
            print(f"Content type: {request.content_type}")
            print(f"Raw request data type: {type(request.data)}")
            print(f"Raw request data keys: {list(request.data.keys()) if isinstance(request.data, dict) else 'Not a dict'}")
            
            product_service = ProductService()
            
            # ENHANCED: Handle different payload structures more robustly
            products_data = None
            
            if isinstance(request.data, list):
                # If data is sent as array directly: [product1, product2, ...]
                products_data = request.data
                print("✅ Data received as direct array")
                
            elif isinstance(request.data, dict):
                if 'products' in request.data:
                    # If data is sent as object: {"products": [product1, product2, ...]}
                    products_data = request.data.get('products', [])
                    print("✅ Data received as object with 'products' key")
                else:
                    # Check if it's a single product object that should be an array
                    if any(key in request.data for key in ['product_name', 'SKU', 'cost_price']):
                        products_data = [request.data]  # Wrap single product in array
                        print("✅ Data received as single product object, wrapped in array")
                    else:
                        # Fallback - try to find products in the data
                        products_data = request.data.get('products', [])
                        print("⚠️ Fallback: trying to extract 'products' key")
            else:
                print("❌ Unknown data format received")
                return Response(
                    {"error": f"Invalid data format. Expected array or object, got {type(request.data)}"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            print(f"Extracted products_data type: {type(products_data)}")
            print(f"Products count: {len(products_data) if isinstance(products_data, list) else 'Not a list'}")
            
            if products_data and isinstance(products_data, list) and len(products_data) > 0:
                print(f"Sample product (first): {products_data[0]}")
            
            # VALIDATION: Check if we have valid data
            if not products_data:
                print("❌ No products provided in request")
                return Response(
                    {"error": "No products provided. Expected 'products' array in request body."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if not isinstance(products_data, list):
                print(f"❌ Products data is not a list: {type(products_data)}")
                return Response(
                    {"error": f"Products data must be an array, got {type(products_data)}"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if len(products_data) == 0:
                print("❌ Empty products array")
                return Response(
                    {"error": "Products array is empty"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            print(f"✅ Calling ProductService.bulk_create_products with {len(products_data)} products")
            
            # Call the service method
            results = product_service.bulk_create_products(products_data)
            
            print(f"✅ Service method returned: {type(results)}")
            print(f"Results keys: {results.keys() if isinstance(results, dict) else 'Not a dict'}")
            print("=== BULK CREATE VIEW DEBUG END ===")
            
            return Response({
                'message': 'Bulk product creation completed',
                'results': results
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            print("=== BULK CREATE VIEW ERROR ===")
            print(f"Error type: {type(e)}")
            print(f"Error message: {str(e)}")
            
            # Print full traceback for debugging
            import traceback
            print("Full traceback:")
            traceback.print_exc()
            print("=== END ERROR DEBUG ===")
            
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ProductImportView(APIView):
    def post(self, request):
        """Import products from CSV/Excel file"""
        try:
            product_service = ProductService()
            
            # Handle file upload
            if 'file' not in request.FILES:
                return Response(
                    {"error": "No file provided"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            uploaded_file = request.FILES['file']
            file_type = uploaded_file.name.split('.')[-1].lower()
            validate_only = request.data.get('validate_only', 'false').lower() == 'true'
            
            # Save file temporarily
            import tempfile
            import os
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{file_type}') as temp_file:
                for chunk in uploaded_file.chunks():
                    temp_file.write(chunk)
                temp_file_path = temp_file.name
            
            try:
                results = product_service.import_products_from_file(
                    temp_file_path, 
                    file_type, 
                    validate_only
                )
                
                return Response({
                    'message': 'Import completed successfully' if not validate_only else 'Validation completed',
                    'results': results
                }, status=status.HTTP_200_OK)
                
            finally:
                # Clean up temporary file
                os.unlink(temp_file_path)
            
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ProductExportView(APIView):
    def get(self, request):
        """Export products to CSV/Excel"""
        try:
            product_service = ProductService()
            file_type = request.GET.get('format', 'csv').lower()
            
            # Get filters
            filters = {}
            if request.GET.get('category_id'):
                filters['category_id'] = request.GET.get('category_id')
            if request.GET.get('status'):
                filters['status'] = request.GET.get('status')
            
            # Get products
            products = product_service.get_all_products(filters if filters else None)
            
            if file_type == 'csv':
                import csv
                from io import StringIO
                
                output = StringIO()
                fieldnames = ['product_name', 'SKU', 'category_id', 'supplier_id', 'stock', 
                             'low_stock_threshold', 'cost_price', 'selling_price', 'unit', 'status']
                writer = csv.DictWriter(output, fieldnames=fieldnames)
                writer.writeheader()
                
                for product in products:
                    row = {field: product.get(field, '') for field in fieldnames}
                    writer.writerow(row)
                
                response = HttpResponse(output.getvalue(), content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="products_export.csv"'
                return response
                
            elif file_type == 'xlsx':
                import pandas as pd
                from io import BytesIO
                
                df = pd.DataFrame(products)
                output = BytesIO()
                df.to_excel(output, index=False)
                output.seek(0)
                
                response = HttpResponse(
                    output.getvalue(),
                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
                response['Content-Disposition'] = 'attachment; filename="products_export.xlsx"'
                return response
            
            else:
                return Response(
                    {"error": "Invalid format. Use 'csv' or 'xlsx'"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ImportTemplateView(APIView):
    def get(self, request):
        """Generate import template file"""
        try:
            product_service = ProductService()
            file_type = request.GET.get('format', 'csv').lower()
            
            template_path = product_service.generate_import_template(file_type)
            
            if file_type == 'csv':
                with open(template_path, 'r') as f:
                    response = HttpResponse(f.read(), content_type='text/csv')
                    response['Content-Disposition'] = 'attachment; filename="product_import_template.csv"'
            else:
                with open(template_path, 'rb') as f:
                    response = HttpResponse(
                        f.read(), 
                        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                    )
                    response['Content-Disposition'] = 'attachment; filename="product_import_template.xlsx"'
            
            # Clean up template file
            import os
            os.unlink(template_path)
            
            return response
            
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
