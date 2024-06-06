# 定义要删除的目录路径
$directoryPath = "output_frames"

# 检查目录是否存在
if (Test-Path -Path $directoryPath) {
    try {
        # 删除目录及其所有内容
        Remove-Item -Path $directoryPath -Recurse -Force
        Write-Output "Directory '$directoryPath' and its contents have been deleted successfully."
    } catch {
        Write-Error "An error occurred while trying to delete the directory: $_"
    }
} else {
    Write-Output "Directory '$directoryPath' does not exist."
}
