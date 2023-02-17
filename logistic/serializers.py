from rest_framework import serializers

from logistic.models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):
    # настройте сериализатор для позиции продукта на складе
    class Meta:
        model = StockProduct
        fields = ['id', 'product', 'quantity', 'price']
        # depth = 1


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['id', 'address', 'products', 'positions']

    def create(self, validated_data):

        print('create', validated_data)
        positions = validated_data.pop('positions')
        stock = super().create(validated_data)
        print('create_stock', stock)

        for position in positions:
            stock_product = StockProduct(
                stock=stock,
                product=position.get('product'),
                quantity=position.get('quantity'),
                price=position.get('price')
            )
            stock_product.save()

        return stock

    def update(self, instance, validated_data):
        print('update_start: instance', instance)
        print('update_start: validated_data', validated_data)
        pre_pos = validated_data.get('positions')

        # for position in pre_pos:
        #     product = position.get('product')
        #     quantity = position.get('quantity')
        #     price = position.get('price')
        #     obj, created = StockProduct.objects.update_or_create(
        #         stock=stock,
        #         product=product,
        #         defaults={'price': price,
        #                   'quantity': quantity}
        #     )
        # return stock


        positions = validated_data.pop('positions')
        stock = super().update(instance, validated_data)
        for position in positions:
            product = position.get('product')
            ob = Product.objects.filter(title=product)
            for i in ob:
                print(i.id)

            # print('product:', product)
            quantity = position.get('quantity')
            price = position.get('price')
            # print(position, product, quantity, price)
            obj, created = StockProduct.objects.update_or_create(
                stock=stock,
                product=product,
                defaults={'price': price,
                          'quantity': quantity}
            )
        return stock
