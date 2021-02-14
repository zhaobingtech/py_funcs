#include "extcode.h"
#ifdef __cplusplus
extern "C" {
#endif

/*!
 * 转化HDF文件
 */
void __cdecl DLL_hdf_convert(char source_input[], 
	int64_t data_mini_batch_size, char path_out[], char ErrorStatus[], 
	int32_t len_path_out, int32_t len_Err_Status);

MgErr __cdecl LVDLLStatus(char *errStr, int errStrLen, void *module);

void __cdecl SetExecuteVIsInPrivateExecutionSystem(Bool32 value);

#ifdef __cplusplus
} // extern "C"
#endif

