from concurrent import futures
import grpc
import glossary_pb2
import glossary_pb2_grpc

# In-memory glossary storage
glossary = {
    "WebAssembly (Wasm)": "Бинарный формат для выполнения программ в веб-браузерах и других окружениях. Обеспечивает высокую производительность благодаря низкоуровневому формату и оптимизированной виртуальной машине.",
    "Node.js": "Среда выполнения JavaScript, основанная на движке V8, позволяющая разрабатывать серверные приложения и выполнять JavaScript вне браузера.",
    "Виртуальная машина (VM)": "Программный компонент, который исполняет байт-код (например, WebAssembly или JavaScript), абстрагируя аппаратное обеспечение и операционную систему.",
    "V8": "Высокопроизводительный JavaScript-движок, разработанный Google, который используется в браузере Chrome и Node.js для выполнения JavaScript и WebAssembly.",
    "JIT-компиляция (Just-In-Time)": "Техника компиляции, при которой байт-код переводится в машинный код на этапе выполнения программы для повышения производительности.",
    "Интерпретатор": "Компонент виртуальной машины, исполняющий байт-код построчно без предварительной компиляции в машинный код.",
    "ABI (Application Binary Interface)": "Интерфейс, определяющий, как функции и данные взаимодействуют между приложением и операционной системой или между модулями программы.",
    "Модуль WebAssembly": "Компилируемая единица, содержащая инструкции и данные WebAssembly, которые можно импортировать и выполнять в различных окружениях.",
    "Эффективность исполнения": "Показатель, определяющий, насколько быстро и с минимальными затратами ресурсов исполняется код в среде выполнения.",
    "Функции FFI (Foreign Function Interface)": "Интерфейс, предоставляющий возможность вызова функций, написанных на других языках, из текущей среды выполнения.",
    "Стек вызовов": "Динамическая структура данных, используемая для хранения информации о функциях, вызванных в процессе выполнения программы, включая аргументы, локальные переменные и адрес возврата.",
    "WebAssembly System Interface (WASI)": "Стандартный интерфейс для взаимодействия WebAssembly с операционной системой, предоставляющий доступ к файловой системе, времени и другим системным ресурсам.",
    "Многопоточность": "Способность среды выполнения выполнять несколько потоков исполнения одновременно, что может быть полезно для повышения производительности WebAssembly в Node.js.",
    "Сравнительный анализ (Benchmarking)": "Методика измерения и сравнения производительности программ, используемая для оценки эффективности исполнения WebAssembly.",
    "Garbage Collection (GC)": "Механизм управления памятью, автоматически освобождающий неиспользуемую память в процессе выполнения программы.",
    "Оптимизация кода": "Процесс улучшения исполняемого кода для повышения его производительности, уменьшения времени выполнения и снижения использования ресурсов.",
    "Энергопотребление": "Параметр, описывающий, сколько энергии потребляет процесс исполнения кода. Может быть важен при сравнении производительности WebAssembly и JavaScript.",
    "Байт-код": "Промежуточное представление программы, исполняемое виртуальной машиной.",
    "Формат бинарного файла": "Представление программ в двоичном виде, оптимизированное для быстрого чтения и выполнения.",
    "Интероперабельность": "Способность различных технологий взаимодействовать друг с другом, например, вызовы функций между JavaScript и WebAssembly."
}

class GlossaryServiceServicer(glossary_pb2_grpc.GlossaryServiceServicer):
    def GetAllTerms(self, request, context):
        return glossary_pb2.TermList(terms=[
            glossary_pb2.Term(name=name, description=desc)
            for name, desc in glossary.items()
        ])

    def AddTerm(self, request, context):
        if request.name in glossary:
            return glossary_pb2.OperationStatus(success=False, message="Term already exists")
        glossary[request.name] = request.description
        return glossary_pb2.OperationStatus(success=True, message="Term added successfully")

    def UpdateTerm(self, request, context):
        if request.name not in glossary:
            return glossary_pb2.OperationStatus(success=False, message="Term not found")
        glossary[request.name] = request.description
        return glossary_pb2.OperationStatus(success=True, message="Term updated successfully")

    def DeleteTerm(self, request, context):
        if request.name not in glossary:
            return glossary_pb2.OperationStatus(success=False, message="Term not found")
        del glossary[request.name]
        return glossary_pb2.OperationStatus(success=True, message="Term deleted successfully")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    glossary_pb2_grpc.add_GlossaryServiceServicer_to_server(GlossaryServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server is running on port 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
