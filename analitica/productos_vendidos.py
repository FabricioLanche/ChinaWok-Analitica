import json
import os
from analitica.athena_client import AthenaQueryExecutor

def handler(event, context):
    """Lambda para consultar los productos más vendidos por local"""
    try:
        # Parsear body
        body = json.loads(event.get('body', '{}'))
        local_id = body.get('local_id', 'LOCAL-0001')  # Por defecto LOCAL-0001
        
        if not local_id:
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'local_id es requerido'})
            }
        
        # Query SQL
        query = f"""
        WITH productos_expandidos AS (
            SELECT 
                local_id,
                pedido_id,
                producto_nombre
            FROM pedidos
            CROSS JOIN UNNEST(productos_nombres) AS t(producto_nombre)
            WHERE local_id = '{local_id}'
        )
        SELECT 
            pe.local_id,
            pe.producto_nombre,
            COUNT(DISTINCT pe.pedido_id) AS pedidos_que_lo_incluyen,
            COUNT(*) AS unidades_vendidas,
            p.categoria,
            ROUND(p.precio, 2) AS precio_unitario_actual,
            ROUND(COUNT(*) * p.precio, 2) AS revenue_total,
            p.stock AS stock_disponible,
            ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS porcentaje_ventas
        FROM productos_expandidos pe
        LEFT JOIN productos p 
            ON pe.local_id = p.local_id 
            AND pe.producto_nombre = p.nombre
        GROUP BY 
            pe.local_id, 
            pe.producto_nombre, 
            p.categoria, 
            p.precio,
            p.stock
        ORDER BY unidades_vendidas DESC, revenue_total DESC
        LIMIT 20;
        """
        
        # Ejecutar query
        executor = AthenaQueryExecutor()
        results = executor.execute_query(query)
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'local_id': local_id,
                'total_productos': len(results),
                'productos': results
            })
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }
