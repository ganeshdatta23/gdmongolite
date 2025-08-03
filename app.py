from gdmongolite.core import DBSingleton

@DBSingleton.on("pre_query")
def log_pre(collection, filt, opts):
    print(f"Querying {collection}: {filt}")

@DBSingleton.on("post_query")
def log_post(collection, result):
    print(f"{collection} query completed.")
