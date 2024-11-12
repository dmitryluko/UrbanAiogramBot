async def get_buying_list():
    return [{'title': f'Product{i}', 'description': f'описание {i}', 'price': i * 100, 'img' : f'food_img_{i}.png'} for i in range(1, 5)]
